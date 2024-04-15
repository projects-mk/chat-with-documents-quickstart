"use client"

import { Sidebar } from "../components/sidebar";
import { TabsDemo } from "../components/tabs";
import { ManageAllResources } from "@/app/pages/resources";
import { About } from "@/app/pages/about";
import { MessagesSquare, InfoIcon, Cog, FileUp } from 'lucide-react';
import React, { useState } from 'react';

const items = [
  { icon: InfoIcon, title: "About"},
  { icon: Cog, title: "Resources"},
  { icon: FileUp, title: "Upload Documents"},
  { icon: MessagesSquare, title: "Chat"}
];

function Index() {
  const [selectedTab, setSelectedTab] = useState(items[0].title);

  const sidebarItems = items.map(item => ({
    ...item,
    onClick: () => {
      setSelectedTab(item.title);
    }
  }));

  return (
    <div className="flex mt-auto">
      <Sidebar 
        title="Chat With Documents" 
        items={sidebarItems} 
      />

      {selectedTab.toLowerCase() === "about" && (
        <div className="flex mt-auto">
          <About />
        </div>
      )}
      {selectedTab.toLowerCase() === "resources" && (
        <div className="flex mt-auto">
          <ManageAllResources />
        </div>
      )}
    </div>
  );
}

export default Index;