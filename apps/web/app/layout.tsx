import "./globals.css";
import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";

import { ShellNavigation } from "../components/layout/shell-navigation";
import { ShellTopbar } from "../components/layout/shell-topbar";

export const metadata: Metadata = {
  title: "全新项目",
  description: "从爆款链接到可执行短视频方案"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>
        <div className="app-shell">
          <aside className="shell-sidebar">
            <div className="shell-sidebar-panel">
              <Link href="/" className="brand">
                <span className="brand-mark">NP</span>
                <span>
                  <strong>全新项目</strong>
                  <span className="brand-copy">AI 短视频工作台</span>
                </span>
              </Link>

              <div className="shell-sidebar-section">
                <p className="shell-sidebar-label">Workspace</p>
                <ShellNavigation />
              </div>

              <div className="shell-sidebar-section shell-sidebar-guide">
                <p className="shell-sidebar-label">MVP Main Flow</p>
                <ol className="shell-flow-list">
                  <li>输入</li>
                  <li>分析</li>
                  <li>预填充工作流</li>
                  <li>运行</li>
                  <li>结果</li>
                  <li>历史</li>
                </ol>
                <p className="shell-sidebar-note">
                  当前外壳只服务这条主链，不引入聊天优先、团队优先或计费优先的页面结构。
                </p>
              </div>
            </div>
          </aside>

          <div className="shell-column">
            <ShellTopbar />
            <div className="shell-content">{children}</div>
          </div>
        </div>
      </body>
    </html>
  );
}
