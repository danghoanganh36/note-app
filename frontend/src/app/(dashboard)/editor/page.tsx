'use client';

import { RichTextEditor } from '@/components/editor/RichTextEditor';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Save, FileText, Share2 } from 'lucide-react';
import { useState } from 'react';

export default function EditorPage() {
  const [title, setTitle] = useState('Untitled Document');
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async (content: string) => {
    console.log('Auto-saving content:', content);
    setIsSaving(true);
    
    // TODO: Save to backend API
    // await fetch('/api/documents', { method: 'POST', body: JSON.stringify({ title, content }) })
    
    setTimeout(() => {
      setIsSaving(false);
    }, 500);
  };

  const handleManualSave = () => {
    console.log('Manual save triggered');
  };

  const handleShare = () => {
    console.log('Share document');
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center gap-3 flex-1">
            <FileText className="h-5 w-5 text-muted-foreground" />
            <Input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="max-w-md border-none text-lg font-medium focus-visible:ring-0 focus-visible:ring-offset-0"
              placeholder="Untitled Document"
            />
          </div>

          <div className="flex items-center gap-2">
            {isSaving && (
              <span className="text-sm text-muted-foreground">Saving...</span>
            )}
            <Button variant="outline" size="sm" onClick={handleShare}>
              <Share2 className="h-4 w-4 mr-2" />
              Share
            </Button>
            <Button size="sm" onClick={handleManualSave}>
              <Save className="h-4 w-4 mr-2" />
              Save
            </Button>
          </div>
        </div>
      </header>

      {/* Editor */}
      <main className="flex-1 overflow-hidden">
        <RichTextEditor
          initialContent="<h1>Welcome to Handbook Compass</h1><p>Start writing your document here...</p>"
          onSave={handleSave}
          autoSaveInterval={5000}
          placeholder="Type '/' for commands..."
        />
      </main>
    </div>
  );
}
