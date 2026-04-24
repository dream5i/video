"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

function getTopbarMeta(pathname: string) {
  if (pathname === "/") {
    return {
      title: "总览视图",
      description: "先看主链健康度、最近运行和当前阶段，再决定要进入哪个项目。"
    };
  }

  if (pathname === "/projects/new") {
    return {
      title: "输入层入口",
      description: "这里负责稳定收口项目输入，不让后续分析、工作流和运行链路散开。"
    };
  }

  if (pathname === "/history") {
    return {
      title: "运行历史",
      description: "这一层负责回看 run 状态、结果沉淀和后续审计挂点。"
    };
  }

  if (pathname.startsWith("/projects/")) {
    return {
      title: "项目工作台",
      description: "把分析、工作流、运行和结果放在同一条主链里收口，避免页面各走各的。"
    };
  }

  return {
    title: "企业级工作台",
    description: "当前外壳先服务主链，不让模板反过来决定业务结构。"
  };
}

export function ShellTopbar() {
  const pathname = usePathname();
  const meta = getTopbarMeta(pathname);

  return (
    <header className="shell-topbar">
      <div className="shell-topbar-copy">
        <p className="eyebrow">Enterprise Workspace</p>
        <div className="shell-topbar-title-row">
          <strong className="shell-topbar-title">{meta.title}</strong>
          <span className="shell-topbar-divider" />
          <span className="shell-topbar-subtitle">{meta.description}</span>
        </div>
      </div>

      <div className="shell-topbar-actions">
        <span className="shell-chip">Contracts First</span>
        <span className="shell-chip">Database Mode</span>
        <Link href="/projects/new" className="button-link shell-quick-link">
          新建项目
        </Link>
      </div>
    </header>
  );
}
