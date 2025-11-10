import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const Header = () => {
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <motion.header 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-slate-900 border-b border-slate-800 py-6 px-4"
      >
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                Visual Similarity Explorer
              </h1>
              <p className="text-slate-400 text-sm md:text-base">
                Powered by CLIP · FastAPI · BentoML · Oracle DB · MinIO
              </p>
            </div>
            <button
              onClick={() => setShowModal(true)}
              className="px-4 py-2 bg-gradient-to-r from-teal-500 to-purple-500 text-white rounded-lg hover:from-teal-600 hover:to-purple-600 transition-all shadow-lg hover:shadow-xl font-medium"
            >
              View System Architecture
            </button>
          </div>
        </div>
      </motion.header>

      <AnimatePresence>
        {showModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
            onClick={() => setShowModal(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-slate-800 rounded-2xl p-6 max-w-4xl w-full shadow-2xl"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-white">System Architecture</h2>
                <button
                  onClick={() => setShowModal(false)}
                  className="text-slate-400 hover:text-white transition-colors text-2xl"
                >
                  ×
                </button>
              </div>
              <div className="bg-slate-900 rounded-lg p-8 flex items-center justify-center min-h-[400px]">
                <img 
                  src="/assets/microservices_architecture.png" 
                  alt="System Architecture Diagram"
                  className="max-w-full max-h-[500px] object-contain rounded-lg"
                />
              </div>
              <p className="text-slate-400 text-sm mt-4 text-center">
                Architecture: Frontend (React) → Backend API (FastAPI) → ML Model (CLIP via BentoML) → Storage (Oracle DB + MinIO)
              </p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default Header;
