# AGENTS.md

## Development approach

- Develop incrementally through small, validated changes.
- Implement only requirements needed by the current milestone.
- Avoid speculative abstractions, directories, interfaces, and dependencies.
- Preserve existing behavior unless a task explicitly requests a behavioral change.
- Inspect existing code and tests before editing.

## Clean Code

- Use precise names that reveal intent.
- Keep methods focused on one responsibility.
- Keep each method at a consistent level of abstraction.
- Extract private methods when they name a meaningful operation or hide lower-level detail.
- Do not extract trivial methods that add navigation without clarity.
- Prefer simple control flow and early validation.
- Remove duplication when doing so preserves clarity.
- Avoid generic modules such as utils.py, helpers.py, or common.py.

## Object-oriented design

- Use classes when they represent domain concepts, maintain meaningful state, or coordinate a cohesive responsibility.
- Do not use inheritance, abstract base classes, protocols, factories, or dependency injection without a demonstrated need.
- Prefer composition over inheritance.
- Prefer immutable domain models where practical.
- Use pure functions when no object state or cohesive object responsibility exists.

## Comments and documentation

- Do not add inline comments.
- Do not add explanatory comments for code that can be clarified through naming and refactoring.
- Do not add docstrings to private methods or self-explanatory classes.
- Public documentation belongs in project documentation when it becomes necessary.

## Types and errors

- Add complete type hints to production code.
- Use domain-specific names instead of generic dictionaries or loosely structured data.
- Raise clear exceptions at system boundaries.
- Do not silently discard invalid input unless the expected behavior explicitly requires it.

## Testing

- Test observable behavior rather than private implementation details.
- Every bug fix or behavioral change must include a test that would previously have failed.
- Keep tests readable and focused.
- Do not weaken tests to make an implementation pass.
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
