"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

function isWorkspaceRoute(pathname: string) {
  return pathname.startsWith("/projects/") && pathname !== "/projects/new";
}

export function ShellNavigation() {
  const pathname = usePathname();
  const workspaceHref = isWorkspaceRoute(pathname) ? pathname : "/projects/proj_demo";

  const items = [
    {
      href: "/",
      label: "总览",
      kicker: "Overview",
      active: pathname === "/"
    },
    {
      href: "/projects/new",
      label: "新建项目",
      kicker: "Intake",
      active: pathname === "/projects/new"
    },
    {
      href: workspaceHref,
      label: "项目工作台",
      kicker: "Workspace",
      active: isWorkspaceRoute(pathname)
    },
    {
      href: "/history",
      label: "运行历史",
      kicker: "History",
      active: pathname === "/history"
    }
  ];

  return (
    <nav className="shell-nav">
      {items.map((item) => (
        <Link
          key={item.label}
          href={item.href}
          className={`shell-nav-link${item.active ? " active" : ""}`}
        >
          <span className="shell-nav-kicker">{item.kicker}</span>
          <strong>{item.label}</strong>
        </Link>
      ))}
    </nav>
  );
}
