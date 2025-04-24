import React from 'react';
import { Brain, GraduationCap } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white border-b border-slate-200 py-3 px-4 sm:px-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <GraduationCap className="h-7 w-7 text-red-600" />
          <h1 className="text-xl font-bold text-slate-800">HyperMath</h1>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="text-sm text-slate-600 hidden sm:inline">Powered by</span>
          <div className="flex items-center bg-gradient-to-r from-blue-500 to-blue-600 text-white px-2 py-1 rounded-md text-sm">
            <Brain className="h-4 w-4 mr-1.5" />
            <span className="font-medium">Gemini + Manim</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;