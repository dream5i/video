"""Baseline schema skeleton for the first persistent MVP tables.

Fill this revision only after the table set is reviewed against:
- docs/database-persistence-and-migration-plan.md
- docs/schema-and-contract-freeze.md
"""

from __future__ import annotations

revision = "20260423_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the first persistent MVP tables."""


def downgrade() -> None:
    """Drop the first persistent MVP tables in reverse order."""
