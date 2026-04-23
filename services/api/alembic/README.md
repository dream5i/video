# Alembic Skeleton

当前目录先保留 migration 骨架，不急着把数据库实现一次做满。

当前约束：

- migration 以 `services/api/alembic/versions/` 为唯一 revision 目录
- schema 设计先服从 `docs/database-persistence-and-migration-plan.md`
- 高风险 migration 必须额外 review pass

当前第一步：

- 先有 baseline revision skeleton
- 再补 SQLAlchemy model
- 最后把 in-memory repository 渐进替换为 persistence adapter
