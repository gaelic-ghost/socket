# Router Customization Flow

## Knobs

- `defaultRoutingPreference`: default route when intent overlaps multiple skills
- `preferPackSuggestions`: include pack suggestions by default
- `installCommandStyle`: command verbosity profile
- `includeAllOption`: include `--all` suggestion by default

## Validation

1. Verify routing suggestions point only to existing skill names.
2. Verify install commands use `gaelic-ghost/apple-dev-skills`.
