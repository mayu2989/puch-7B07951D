import React, { useState, useRef } from 'react';
import { FileUpIcon, MusicIcon, Loader2Icon, ErrorIcon } from './components/Icons';

// Interface for the resume analysis results
interface ResumeResults {
  score: string;
  completeness: string;
  suggestions: string[];
}

// Interface for music suggestions
interface MusicSuggestion {
  title: string;
  artist: string;
  albumArt: string;
}

const App: React.FC = () => {
  // State to manage the active tab: 'resume' or 'music'
  const [activeTab, setActiveTab] = useState<'resume' | 'music'>('resume');
  
  // State to manage the resume file, can be File or null
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  
  // State to manage the analysis results, can be ResumeResults or null
  const [resumeResults, setResumeResults] = useState<ResumeResults | null>(null);
  
  // State to manage the loading state for resume analysis
  const [resumeLoading, setResumeLoading] = useState<boolean>(false);
  
  // State for mood text input
  const [moodText, setMoodText] = useState<string>('');
  
  // State for music suggestions, can be an array of MusicSuggestion or null
  const [musicSuggestions, setMusicSuggestions] = useState<MusicSuggestion[] | null>(null);
  
  // State for music suggestion loading
  const [musicLoading, setMusicLoading] = useState<boolean>(false);
  
  // State for error messages, can be a string or null
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // A ref for the file input element, specifying its type
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Function to handle file drop event
  const handleFileDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files.length) {
      setResumeFile(e.dataTransfer.files[0]);
    }
  };

  // Function to handle file selection via the file dialog
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length) {
      setResumeFile(e.target.files[0]);
    }
  };

  // Function to simulate a resume analysis API call
  const analyzeResume = async () => {
    if (!resumeFile) {
      setErrorMessage('Please upload a resume file first.');
      return;
    }
    setResumeLoading(true);
    setErrorMessage(null);

    // Mock API call using setTimeout to simulate a network request
    setTimeout(() => {
      // Mock data for the resume analysis results
      const mockResults: ResumeResults = {
        score: '85%',
        completeness: 'Your resume is 95% complete. It includes sections for Experience, Education, and Skills.',
        suggestions: [
          'Add quantifiable achievements to your work experience.',
          'Tailor your skills section to the job description you are applying for.',
          'Consider a more modern font to improve readability.',
        ],
      };
      setResumeResults(mockResults);
      setResumeLoading(false);
    }, 2000);
  };
  
  // A placeholder function to fetch music suggestions
  const getMusicSuggestions = async () => {
    if (!moodText.trim()) {
      setErrorMessage('Please enter your mood or feelings to get a suggestion.');
      return;
    }

    setMusicLoading(true);
    setErrorMessage(null);

    // This is a placeholder for a real API call to a model like Gemini
    // For this frontend, we'll just simulate a delay and use mock data.
    setTimeout(() => {
      const mockSuggestions: MusicSuggestion[] = [
        {
          title: 'A Beautiful Day',
          artist: 'The Bright Tones',
          albumArt: 'https://placehold.co/150x150/dbeafe/1e3a8a?text=Happy',
        },
        {
          title: 'Sunshine Groove',
          artist: 'Funkadelic Flow',
          albumArt: 'https://placehold.co/150x150/fde68a/92400e?text=Groovy',
        },
        {
          title: 'Morning Coffee',
          artist: 'Acoustic Soul',
          albumArt: 'https://placehold.co/150x150/dcfce7/065f46?text=Calm',
        },
      ];
      setMusicSuggestions(mockSuggestions);
      setMusicLoading(false);
    }, 2000);
  };
  
  // Main App Component with UI logic and rendering
  return (
    <div className="min-h-screen bg-neutral-100 dark:bg-neutral-900 text-neutral-800 dark:text-neutral-200 flex items-center justify-center p-4">
      {/* Main container card */}
      <div className="bg-white dark:bg-neutral-800 rounded-2xl shadow-2xl overflow-hidden max-w-4xl w-full p-6 sm:p-10 transition-all duration-300 transform scale-95 hover:scale-100">
        {/* Header and Title */}
        <div className="flex flex-col sm:flex-row justify-between items-center mb-8 border-b pb-4 dark:border-neutral-700">
          <h1 className="text-3xl sm:text-4xl font-extrabold text-indigo-600 dark:text-indigo-400">
            Hackathon Hub
          </h1>
          <p className="text-sm text-neutral-500 mt-2 sm:mt-0">
            Your all-in-one productivity and creativity tool.
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex justify-center gap-4 sm:gap-8 mb-8">
          <button
            onClick={() => { setActiveTab('resume'); setResumeResults(null); setResumeFile(null); setErrorMessage(null); }}
            className={`flex items-center gap-2 px-4 py-2 sm:px-6 sm:py-3 rounded-full text-sm font-semibold transition-all duration-300 transform hover:scale-105 ${
              activeTab === 'resume'
                ? 'bg-indigo-600 text-white shadow-lg'
                : 'bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-300 dark:hover:bg-neutral-600'
            }`}
          >
            <FileUpIcon className="w-5 h-5" />
            Resume Checker
          </button>
          <button
            onClick={() => { setActiveTab('music'); setMusicSuggestions(null); setMoodText(''); setErrorMessage(null); }}
            className={`flex items-center gap-2 px-4 py-2 sm:px-6 sm:py-3 rounded-full text-sm font-semibold transition-all duration-300 transform hover:scale-105 ${
              activeTab === 'music'
                ? 'bg-indigo-600 text-white shadow-lg'
                : 'bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-300 dark:hover:bg-neutral-600'
            }`}
          >
            <MusicIcon className="w-5 h-5" />
            Music Suggestor
          </button>
        </div>

        {/* Dynamic Content based on active tab */}
        {activeTab === 'resume' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-center">Resume Analyzer</h2>
            <p className="text-neutral-500 text-center">
              Upload your resume and get instant feedback on its quality and completeness.
            </p>

            {/* File Upload Area */}
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleFileDrop}
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-neutral-300 dark:border-neutral-600 rounded-xl p-8 text-center cursor-pointer transition-colors duration-300 hover:border-indigo-500 hover:bg-indigo-50 dark:hover:bg-indigo-950"
            >
              <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                onChange={handleFileSelect}
                accept=".pdf,.docx"
              />
              <FileUpIcon className="mx-auto w-10 h-10 text-indigo-500 mb-4" />
              {resumeFile ? (
                <p className="text-neutral-700 dark:text-neutral-300 font-medium">{resumeFile.name}</p>
              ) : (
                <p className="text-neutral-500">
                  Drag and drop your resume here, or <span className="text-indigo-500 font-semibold">click to browse</span>
                </p>
              )}
            </div>
            
            {/* Error Message Display */}
            {errorMessage && (
              <div className="bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300 p-4 rounded-xl flex items-center gap-3">
                <ErrorIcon className="w-5 h-5" />
                <span>{errorMessage}</span>
              </div>
            )}

            {/* Analyze Button */}
            <button
              onClick={analyzeResume}
              disabled={!resumeFile || resumeLoading}
              className="w-full flex items-center justify-center gap-2 py-3 bg-indigo-600 text-white rounded-xl font-semibold shadow-md transition-all duration-300 hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed"
            >
              {resumeLoading && <Loader2Icon className="animate-spin w-5 h-5" />}
              {resumeLoading ? 'Analyzing...' : 'Analyze My Resume'}
            </button>

            {/* Resume Analysis Results */}
            {resumeResults && (
              <div className="mt-8 p-6 bg-neutral-50 dark:bg-neutral-700 rounded-xl shadow-inner">
                <h3 className="text-xl font-bold mb-4">Analysis Results</h3>
                <div className="space-y-4">
                  <div className="bg-white dark:bg-neutral-800 p-4 rounded-lg">
                    <p className="font-semibold text-lg text-indigo-600 dark:text-indigo-400">Quality Score: {resumeResults.score}</p>
                  </div>
                  <div className="bg-white dark:bg-neutral-800 p-4 rounded-lg">
                    <p className="font-semibold mb-2">Completeness</p>
                    <p className="text-neutral-600 dark:text-neutral-400">{resumeResults.completeness}</p>
                  </div>
                  <div className="bg-white dark:bg-neutral-800 p-4 rounded-lg">
                    <p className="font-semibold mb-2">Suggestions for Improvement</p>
                    <ul className="list-disc list-inside space-y-1 text-neutral-600 dark:text-neutral-400">
                      {resumeResults.suggestions.map((suggestion, index) => (
                        <li key={index}>{suggestion}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'music' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-center">Emotional Music Suggestor</h2>
            <p className="text-neutral-500 text-center">
              Describe your current mood and get a playlist of songs tailored to how you feel.
            </p>

            {/* Mood Text Input Area */}
            <div className="relative">
              <textarea
                value={moodText}
                onChange={(e) => setMoodText(e.target.value)}
                placeholder="How are you feeling today? (e.g., 'energetic', 'calm and relaxed', 'a bit sad')"
                className="w-full h-32 p-4 text-sm bg-neutral-100 dark:bg-neutral-700 rounded-xl border-2 border-neutral-300 dark:border-neutral-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-200 resize-none"
              ></textarea>
            </div>
            
            {/* Error Message Display */}
            {errorMessage && (
              <div className="bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300 p-4 rounded-xl flex items-center gap-3">
                <ErrorIcon className="w-5 h-5" />
                <span>{errorMessage}</span>
              </div>
            )}

            {/* Suggest Music Button */}
            <button
              onClick={getMusicSuggestions}
              disabled={!moodText.trim() || musicLoading}
              className="w-full flex items-center justify-center gap-2 py-3 bg-indigo-600 text-white rounded-xl font-semibold shadow-md transition-all duration-300 hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed"
            >
              {musicLoading && <Loader2Icon className="animate-spin w-5 h-5" />}
              {musicLoading ? 'Suggesting...' : 'Suggest Music'}
            </button>

            {/* Music Suggestions */}
            {musicSuggestions && (
              <div className="mt-8 p-6 bg-neutral-50 dark:bg-neutral-700 rounded-xl shadow-inner">
                <h3 className="text-xl font-bold mb-4">Music Suggestions for Your Mood</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {musicSuggestions.map((song, index) => (
                    <div
                      key={index}
                      className="bg-white dark:bg-neutral-800 rounded-xl shadow-md p-4 flex items-center gap-4 transition-all duration-300 transform hover:scale-105"
                    >
                      <img
                        src={song.albumArt}
                        alt="Album Art"
                        className="w-16 h-16 rounded-lg object-cover"
                      />
                      <div>
                        <p className="font-semibold">{song.title}</p>
                        <p className="text-neutral-500 text-sm">{song.artist}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
