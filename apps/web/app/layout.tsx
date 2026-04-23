import "./globals.css";
import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "全新项目",
  description: "从爆款链接到可执行短视频方案"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>
        <div className="app-shell">
          <header className="topbar">
            <Link href="/" className="brand">
              <span className="brand-mark">NP</span>
              <span>
                <strong>全新项目</strong>
                <span className="brand-copy">AI 短视频工作台</span>
              </span>
            </Link>
            <nav className="nav">
              <Link href="/" className="nav-link">
                总览
              </Link>
              <Link href="/projects/new" className="nav-link">
                新建项目
              </Link>
              <Link href="/projects/proj_demo" className="nav-link">
                演示项目
              </Link>
              <Link href="/history" className="nav-link">
                历史
              </Link>
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
