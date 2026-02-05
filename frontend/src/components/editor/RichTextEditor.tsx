'use client';

import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Placeholder from '@tiptap/extension-placeholder';
import Underline from '@tiptap/extension-underline';
import TextAlign from '@tiptap/extension-text-align';
import Link from '@tiptap/extension-link';
import Image from '@tiptap/extension-image';
import { EditorToolbar } from './EditorToolbar';
import { useEffect, useState } from 'react';

interface RichTextEditorProps {
  initialContent?: string;
  onSave?: (content: string) => void;
  autoSaveInterval?: number;
  placeholder?: string;
}

export function RichTextEditor({
  initialContent = '',
  onSave,
  autoSaveInterval = 5000,
  placeholder = 'Start writing...',
}: RichTextEditorProps) {
  const [content, setContent] = useState(initialContent);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);

  const editor = useEditor({
    immediatelyRender: false,
    extensions: [
      StarterKit.configure({
        heading: {
          levels: [1, 2, 3],
        },
      }),
      Placeholder.configure({
        placeholder,
      }),
      Underline,
      TextAlign.configure({
        types: ['heading', 'paragraph'],
      }),
      Link.configure({
        openOnClick: false,
        HTMLAttributes: {
          class: 'text-blue-500 underline cursor-pointer hover:text-blue-600',
        },
      }),
      Image.configure({
        HTMLAttributes: {
          class: 'rounded-lg max-w-full h-auto my-4',
        },
      }),
    ],
    content: initialContent,
    editorProps: {
      attributes: {
        class:
          'prose prose-sm sm:prose lg:prose-lg dark:prose-invert focus:outline-none max-w-none p-8 min-h-[calc(100vh-200px)]',
      },
    },
    onUpdate: ({ editor }) => {
      const html = editor.getHTML();
      setContent(html);
    },
  });

  // Auto-save
  useEffect(() => {
    if (!onSave || !content) return;

    const timer = setTimeout(() => {
      onSave(content);
      setLastSaved(new Date());
    }, autoSaveInterval);

    return () => clearTimeout(timer);
  }, [content, onSave, autoSaveInterval]);

  return (
    <div className="flex flex-col h-full">
      <EditorToolbar editor={editor} />
      
      <div className="flex-1 overflow-y-auto bg-background">
        <EditorContent editor={editor} className="h-full" />
      </div>

      {lastSaved && (
        <div className="text-xs text-muted-foreground p-2 border-t text-center">
          Last saved: {lastSaved.toLocaleTimeString()}
        </div>
      )}
    </div>
  );
}
