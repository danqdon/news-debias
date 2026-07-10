# AGENTS.md

## Development approach

- Develop incrementally through small, validated changes.
- Implement only requirements needed by the current milestone.
- Prefer the smallest implementation that clearly expresses the required behavior.
- Avoid speculative abstractions, directories, interfaces, and dependencies.
- Preserve existing behavior unless a task explicitly requests a behavioral change.
- Inspect existing code and tests before editing.

## Clean Code

- Use precise names that reveal intent.
- Use straightforward control flow.
- Prefer readable standard-library operations over lower-level manual code when they express the same intention more clearly.
- Do not retain defensive logic for cases the current design cannot produce.
- Do not add indirection unless it makes the caller easier to understand.
- Keep each method at a consistent level of abstraction.
- Extract private methods when they name a meaningful operation or hide lower-level detail.
- Do not extract trivial methods that add navigation without clarity.
- Remove duplication when doing so preserves clarity.
- Avoid generic modules such as utils.py, helpers.py, or common.py.

## Object-oriented design

- Keep processing services stateless unless state is genuinely part of their responsibility.
- Pass input data through method arguments instead of storing temporary processing input on the object.
- Use classes when they represent domain concepts or improve cohesion and readability.
- Do not use inheritance, abstract base classes, protocols, factories, or dependency injection without a demonstrated need.
- Prefer composition over inheritance.
- Prefer immutable domain models where practical.
- Use pure functions when no object state or cohesive object responsibility exists.

## Comments and documentation

- Do not add explanatory comments for code that can be clarified through naming and refactoring.
- Do not add inline comments.
- Do not add docstrings to private methods or self-explanatory classes.
- Keep documentation focused on behavior, architecture decisions, and project usage.

## Types and errors

- Add complete type hints to production code.
- Use domain-specific names instead of generic dictionaries or loosely structured data.
- Raise clear exceptions at system boundaries.
- Do not silently discard invalid input unless the expected behavior explicitly requires it.

## Testing

- Test observable behavior rather than private implementation details.
- Protect important invariants such as exact text offsets.
- Every bug fix or behavioral change must include a test that would previously have failed.
- Keep tests readable and focused.
- Do not weaken tests to make an implementation pass.
- Add tests when they protect a real edge case or behavioral requirement.
- Avoid mocking when deterministic real objects are sufficient.

## Dependencies and architecture

- Do not add a dependency when the standard library is sufficient.
- Do not add frameworks or infrastructure before there is a demonstrated requirement.
- Keep domain and processing logic independent of future interfaces such as CLI, web UI, databases, and external AI providers.
- Do not reorganize unrelated files during a focused change.

## Quality checks

Before completing any code change, run:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

All checks must pass.
