'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { clearApiToken } from '@/lib/api-config';
import { useCurrentUser } from '@/hooks/useCurrentUser';

// Mock data
const mockDocuments = [
  { id: '1', title: 'Getting Started', emoji: '🚀', updatedAt: '2 hours ago', access: 'private' },
  { id: '2', title: 'Project Roadmap', emoji: '🗺️', updatedAt: 'Yesterday', access: 'shared' },
  { id: '3', title: 'Meeting Notes', emoji: '📝', updatedAt: '3 days ago', access: 'private' },
  { id: '4', title: 'Design System', emoji: '🎨', updatedAt: 'Last week', access: 'public' },
  { id: '5', title: 'API Documentation', emoji: '📚', updatedAt: '2 weeks ago', access: 'shared' },
];

const mockFolders = [
  { id: 'f1', name: 'Personal', icon: '👤', count: 5 },
  { id: 'f2', name: 'Work', icon: '💼', count: 12 },
  { id: 'f3', name: 'Archive', icon: '📦', count: 23 },
];

export default function DashboardPage() {
  const router = useRouter();
  const { user, isLoading: isLoadingUser } = useCurrentUser();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFolder, setSelectedFolder] = useState<string | null>(null);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const filteredDocuments = mockDocuments.filter(doc =>
    doc.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleLogout = async () => {
    setIsLoggingOut(true);
    
    await new Promise(resolve => setTimeout(resolve, 500));
    
    clearApiToken();
    router.push('/');
  };

  const getUserInitials = () => {
    if (!user) return 'U';
    if (user.display_name) {
      const names = user.display_name.split(' ');
      if (names.length >= 2) {
        return `${names[0][0]}${names[1][0]}`.toUpperCase();
      }
      return user.display_name.substring(0, 2).toUpperCase();
    }
    return user.email.substring(0, 2).toUpperCase();
  };

  if (isLoadingUser) {
    return (
      <div className="flex h-screen items-center justify-center bg-white">
        <div className="text-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-200 border-t-gray-900 mx-auto"></div>
          <p className="mt-4 text-sm text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-white">
      <aside className="w-60 flex-shrink-0 border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="flex w-full items-center space-x-3 rounded-md px-2 py-1.5 hover:bg-gray-100 transition-colors">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={user?.avatar_url || undefined} />
                  <AvatarFallback>{getUserInitials()}</AvatarFallback>
                </Avatar>
                <div className="flex-1 text-left">
                  <p className="text-sm font-medium text-gray-900">
                    {user?.display_name || user?.email.split('@')[0] || 'User'}
                  </p>
                  <p className="text-xs text-gray-500">Free Plan</p>
                </div>
                <svg className="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" className="w-56">
              <DropdownMenuItem><span>Profile</span></DropdownMenuItem>
              <DropdownMenuItem><span>Settings</span></DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem><span>Upgrade to Pro</span></DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem className="text-red-600 cursor-pointer" onClick={handleLogout} disabled={isLoggingOut}>
                <span>{isLoggingOut ? 'Logging out...' : 'Log out'}</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>

        <nav className="flex-1 space-y-1 p-3 overflow-y-auto">
          <div className="space-y-1">
            <Link href="/dashboard" className="flex items-center space-x-2 rounded-md px-3 py-2 text-sm font-medium bg-gray-100 text-gray-900 transition-colors">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <span>Home</span>
            </Link>
            <Link href="/editor" className="flex items-center space-x-2 rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              <span>Editor</span>
            </Link>
            <Link href="/dashboard/search" className="flex items-center space-x-2 rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span>Search</span>
            </Link>
            <Link href="/dashboard/shared" className="flex items-center space-x-2 rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span>Shared with me</span>
            </Link>
          </div>

          <div className="pt-4">
            <div className="flex items-center justify-between px-3 py-2">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Folders</span>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <button className="text-gray-400 hover:text-gray-600 transition-colors">
                    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                  </button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-48">
                  <DropdownMenuItem className="cursor-pointer">
                    <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span>New Document</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem className="cursor-pointer">
                    <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                    </svg>
                    <span>New Folder</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
            <div className="space-y-1">
              {mockFolders.map((folder) => (
                <div
                  key={folder.id}
                  className={`group flex w-full items-center justify-between rounded-md px-3 py-2 text-sm transition-colors ${
                    selectedFolder === folder.id ? 'bg-gray-100 text-gray-900' : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <button
                    onClick={() => setSelectedFolder(folder.id)}
                    className="flex flex-1 items-center space-x-2"
                  >
                    <span>{folder.icon}</span>
                    <span>{folder.name}</span>
                  </button>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-gray-500">{folder.count}</span>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <button className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-gray-600 transition-all">
                          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                          </svg>
                        </button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end" className="w-48">
                        <DropdownMenuItem className="cursor-pointer">
                          <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                          <span>New Document</span>
                        </DropdownMenuItem>
                        <DropdownMenuItem className="cursor-pointer">
                          <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                          </svg>
                          <span>New Folder</span>
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem className="cursor-pointer">
                          <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                          <span>Rename</span>
                        </DropdownMenuItem>
                        <DropdownMenuItem className="cursor-pointer text-red-600">
                          <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                          <span>Delete</span>
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </nav>
      </aside>

      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="border-b border-gray-200 bg-white">
          <div className="px-8 py-4">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-semibold text-gray-900">Home</h1>
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <svg className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  <Input
                    type="search"
                    placeholder="Search documents..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="h-10 w-80 pl-10 border-gray-300 focus:border-gray-900 focus:ring-gray-900"
                  />
                </div>
              </div>
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto bg-gray-50">
          <div className="mx-auto max-w-7xl px-8 py-8">
            <div className="mb-8 grid grid-cols-3 gap-4">
              <div className="rounded-lg border border-gray-200 bg-white p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Documents</p>
                    <p className="mt-1 text-2xl font-semibold text-gray-900">24</p>
                  </div>
                  <div className="rounded-lg bg-gray-100 p-3">
                    <svg className="h-6 w-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                </div>
              </div>
              <div className="rounded-lg border border-gray-200 bg-white p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Shared</p>
                    <p className="mt-1 text-2xl font-semibold text-gray-900">7</p>
                  </div>
                  <div className="rounded-lg bg-gray-100 p-3">
                    <svg className="h-6 w-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                </div>
              </div>
              <div className="rounded-lg border border-gray-200 bg-white p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Quizzes</p>
                    <p className="mt-1 text-2xl font-semibold text-gray-900">12</p>
                  </div>
                  <div className="rounded-lg bg-gray-100 p-3">
                    <svg className="h-6 w-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">Recent Documents</h2>
                <Link href="/dashboard/documents" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">
                  View all →
                </Link>
              </div>
              <div className="grid gap-3">
                {filteredDocuments.map((doc) => (
                  <Link
                    key={doc.id}
                    href={`/dashboard/documents/${doc.id}`}
                    className="group flex items-center justify-between rounded-lg border border-gray-200 bg-white p-4 hover:border-gray-300 hover:shadow-sm transition-all"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-md bg-gray-100 text-xl">
                        {doc.emoji}
                      </div>
                      <div>
                        <h3 className="font-medium text-gray-900 group-hover:text-gray-700 transition-colors">{doc.title}</h3>
                        <p className="text-sm text-gray-500">Updated {doc.updatedAt}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800">
                        {doc.access}
                      </span>
                      <svg className="h-5 w-5 text-gray-400 group-hover:text-gray-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </Link>
                ))}
              </div>
            </div>

            {filteredDocuments.length === 0 && (
              <div className="mt-12 text-center">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No documents found</h3>
                <p className="mt-1 text-sm text-gray-500">Try adjusting your search query.</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
