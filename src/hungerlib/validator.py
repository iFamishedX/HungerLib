from dataclasses import fields
from .utils.exceptions import FatalValidationError, ValidationFallbacks


class Validator:
    """
    Generic rules-driven validator for datamap-based config objects.

    Performs ONLY:
    - type checking
    - missing key checking
    - fallback usage checking
    - rule checking (required / recommended / optional)
    - message templating

    No domain-specific validation.
    """

    def __init__(
        self,
        msg_missing_required="{field}: missing required key",
        msg_missing_recommended="{field}: key missing, using fallback {fallback}",
        msg_fallback_required="{field}: must not use fallback (got {value})",
        msg_fallback_recommended="{field}: using fallback {value}",
        msg_type_mismatch="{schema}.{field}: expected {expected}, got {actual} ({value!r})",
    ):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.defaults: list[str] = []

        # message templates
        self.msg_missing_required = msg_missing_required
        self.msg_missing_recommended = msg_missing_recommended
        self.msg_fallback_required = msg_fallback_required
        self.msg_fallback_recommended = msg_fallback_recommended
        self.msg_type_mismatch = msg_type_mismatch

    # type checking
    def validate_key_types(self, config_obj, schema):
        for f in fields(schema):
            if f.name.startswith("__"):
                continue

            expected = f.type
            value = getattr(config_obj, f.name, None)

            if value is None:
                continue

            try:
                if not isinstance(value, expected):
                    self.errors.append(
                        self.msg_type_mismatch.format(
                            schema=schema.__name__,
                            field=f.name,
                            expected=getattr(expected, "__name__", str(expected)),
                            actual=type(value).__name__,
                            value=value,
                        )
                    )
            except TypeError:
                # ignore typing constructs that break isinstance
                pass

    # rule lookup
    def _get_rule_level(self, config_obj, name: str) -> str:
        rules = getattr(config_obj.__class__, "rules", None)
        if rules is None:
            return "optional"
        return getattr(rules, name, "optional")

    # field checking
    def check_field(self, config_obj, name: str):
        raw = getattr(config_obj, "raw", None)
        fb = getattr(config_obj, "fallbacks", None)

        if raw is None or fb is None:
            return

        val = getattr(config_obj, name)
        raw_val = getattr(raw, name)
        fb_val = getattr(fb, name)

        level = self._get_rule_level(config_obj, name)

        # missing YAML key
        if raw_val is None:
            if level == "required":
                self.errors.append(
                    self.msg_missing_required.format(field=name)
                )
            elif level == "recommended":
                self.warnings.append(
                    self.msg_missing_recommended.format(field=name, fallback=fb_val)
                )
            return

        # fallback usage
        if fb_val is not None and val == fb_val:
            if level == "required":
                self.errors.append(
                    self.msg_fallback_required.format(field=name, value=val)
                )
            elif level == "recommended":
                self.warnings.append(
                    self.msg_fallback_recommended.format(field=name, value=val)
                )

    # subclass hook
    def validate_schema(self, config_obj):
        pass

    # orchestration
    def run(self, *configs):
        for cfg in configs:
            self.validate_schema(cfg)

        if self.errors:
            raise FatalValidationError(self.format_report())

        if self.defaults:
            raise ValidationFallbacks(self.format_report())

        return self.format_report()

    # reporting
    def format_report(self) -> str:
        out = []

        if self.errors:
            out.append("Errors:")
            for e in self.errors:
                out.append(f" - {e}")

        if self.defaults:
            out.append("Defaults:")
            for d in self.defaults:
                out.append(f" - {d}")

        if self.warnings:
            out.append("Warnings:")
            for w in self.warnings:
                out.append(f" - {w}")

        if not out:
            return "All configs are valid."

        return "\n".join(out)
