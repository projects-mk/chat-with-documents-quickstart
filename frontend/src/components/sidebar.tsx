"use client"

import React, { useState } from 'react';
import { Separator } from "@/components/ui/separator"

interface SidebarItemProps {
  icon: React.ElementType;
  title: string;
  active?: boolean;
  onClick?: () => void;
};

type SidebarProps = {
  title: string;
  items: SidebarItemProps[];
};

function SidebarItem({ icon: Icon, title, active=false, onClick }: SidebarItemProps) {
  return (
    <li>
      <a
        href={`#${title.toLowerCase()}`}
        onClick={onClick}
        className={`flex items-center rounded-lg px-3 py-2 text-slate-900 hover:bg-slate-100 dark:text-white dark:hover:bg-slate-700 ${
          active ? "bg-slate-100 dark:bg-slate-700" : ""
        }`}
      >
        <Icon />
        <span className="ml-3 flex-1 whitespace-nowrap">{title}</span>
      </a>
    </li>
  );
}

function Sidebar({ title, items }: SidebarProps) {
  const [sidebarItems, setSidebarItems] = useState(items);

    const onClick = (index: number) => {
      const newItems = sidebarItems.map((item, i) => ({
        ...item,
        active: i === index,
      }));
      setSidebarItems(newItems);

      const handleClick = sidebarItems[index].onClick;
      if (handleClick) {
        handleClick();
      }
    };

  return (
    <div className=" w-1/3 bg-white dark:bg-slate-900">
      <aside id="sidebar" className="fixed left-0 top-0 z-40 h-1/2 w-64 transition-transform" aria-label="Sidebar">
        <div className="flex h-full flex-col overflow-y-auto border-r border-slate-200 bg-white px-3 py-4 dark:border-slate-700 dark:bg-slate-900">
          <div className="mb-10 flex items-center rounded-lg px-3 py-2 text-slate-900 dark:text-white">
            <span className="ml-3 text-base font-semibold">{title}
            <Separator />
            </span>
          </div>
          <ul className="space-y-2">
            {sidebarItems.map((item, index) => (
              <SidebarItem key={index} {...item} onClick={() => onClick(index)} />
            ))}
          </ul>
        </div>
      </aside>
    </div>
  );
}

export { Sidebar };
