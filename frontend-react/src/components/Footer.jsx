import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-slate-900 border-t border-slate-800 py-8 px-4 mt-16">
      <div className="max-w-7xl mx-auto text-center">
        <p className="text-slate-300 font-medium mb-3">
          Built by{' '}
          <a
            href="https://github.com/Abdeljalil-Ounaceur"
            target="_blank"
            rel="noopener noreferrer"
            className="text-teal-400 hover:text-teal-300 transition-colors"
          >
            Abdeljalil Ounaceur
          </a>
        </p>
        <div className="flex flex-wrap justify-center gap-3 text-sm text-slate-400">
          <span className="px-3 py-1 bg-slate-800 rounded-full">React</span>
          <span className="px-3 py-1 bg-slate-800 rounded-full">Tailwind CSS</span>
          <span className="px-3 py-1 bg-slate-800 rounded-full">Framer Motion</span>
          <span className="px-3 py-1 bg-slate-800 rounded-full">FastAPI</span>
          <span className="px-3 py-1 bg-slate-800 rounded-full">CLIP</span>
          <span className="px-3 py-1 bg-slate-800 rounded-full">BentoML</span>
          <span className="px-3 py-1 bg-slate-800 rounded-full">Oracle DB</span>
          <span className="px-3 py-1 bg-slate-800 rounded-full">MinIO</span>
        </div>
        <p className="text-slate-500 text-xs mt-4">
          AI-powered visual similarity search platform
        </p>
      </div>
    </footer>
  );
};

export default Footer;
