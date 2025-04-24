import React, { useState } from 'react';
import { Code, Volume2, VolumeX } from 'lucide-react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';

interface VideoPlayerProps {
  videoUrl: string | null;
  codeSnippet: string | null;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ videoUrl, codeSnippet }) => {
  const [showCode, setShowCode] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  
  if (!videoUrl) {
    return (
      <div className="flex items-center justify-center h-full p-6">
        <p className="text-slate-500 text-center">No video available yet. Ask a question to generate a visualization.</p>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 bg-white border-b border-slate-200">
        <h2 className="text-lg font-semibold text-slate-800">Visual Explanation</h2>
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="p-4 space-y-4">
          <div className="relative bg-black rounded-lg overflow-hidden shadow-md">
            <video 
              src={videoUrl} 
              controls 
              autoPlay
              muted={isMuted}
              loop
              className="w-full h-auto"
            >
              Your browser does not support the video tag.
            </video>
            <button 
              onClick={() => setIsMuted(!isMuted)}
              className="absolute bottom-4 right-4 bg-black/70 p-2 rounded-full text-white hover:bg-black/90"
            >
              {isMuted ? <VolumeX className="h-5 w-5" /> : <Volume2 className="h-5 w-5" />}
            </button>
          </div>

          {codeSnippet && (
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <h3 className="text-md font-medium text-slate-700">Generated Manim Code</h3>
                <button 
                  onClick={() => setShowCode(!showCode)}
                  className="flex items-center space-x-1.5 text-sm text-indigo-600 hover:text-indigo-700"
                >
                  <Code className="h-4 w-4" />
                  <span>{showCode ? 'Hide Code' : 'Show Code'}</span>
                </button>
              </div>

              {showCode && (
                <div className="rounded-md overflow-hidden">
                  <SyntaxHighlighter 
                    language="python" 
                    style={atomOneDark}
                    customStyle={{ margin: 0 }}
                    showLineNumbers
                  >
                    {codeSnippet}
                  </SyntaxHighlighter>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;