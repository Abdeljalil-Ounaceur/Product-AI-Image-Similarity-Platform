import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';

const SAMPLE_IMAGES = [
  { name: 'Dada Style', path: '/mock-images/a man riding a horse dada.png' },
  { name: 'Studio Ghibli', path: '/mock-images/a man riding a horse studio ghibli.png' },
  { name: 'Anime Style', path: '/mock-images/anime.png' },
  { name: 'Cinematic', path: '/mock-images/cinematic.png' },
];

const UploadSection = ({ onSubmit, onReset, hasResults, uploadedImageUrl }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = useCallback((file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  }, []);

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    handleFileChange(file);
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFileChange(file);
  }, [handleFileChange]);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleSubmit = () => {
    if (selectedFile) {
      onSubmit(selectedFile);
    }
  };

  const handleSampleClick = async (imagePath) => {
    try {
      const response = await fetch(imagePath);
      const blob = await response.blob();
      const fileName = imagePath.split('/').pop();
      const file = new File([blob], fileName, { type: blob.type });
      
      setSelectedFile(file);
      setPreviewUrl(imagePath);
      
      setTimeout(() => {
        onSubmit(file);
      }, 300);
    } catch (error) {
      console.error('Error loading sample image:', error);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    if (onReset) {
      onReset();
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ 
        opacity: 1, 
        y: 0,
        scale: hasResults ? 0.95 : 1,
        marginTop: hasResults ? '0' : '40px'
      }}
      transition={{ duration: 0.5 }}
      className={`max-w-4xl mx-auto px-4 ${hasResults ? 'mb-6' : 'mb-12'}`}
    >
      {hasResults && uploadedImageUrl && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-slate-800 rounded-2xl p-4 mb-4 flex items-center justify-between shadow-lg border border-slate-700"
        >
          <div className="flex items-center gap-4">
            <img
              src={uploadedImageUrl}
              alt="Uploaded"
              className="w-16 h-16 object-cover rounded-lg"
            />
            <div>
              <p className="text-white font-medium">Your uploaded image</p>
              <p className="text-slate-400 text-sm">{selectedFile?.name || 'Sample image'}</p>
            </div>
          </div>
          <button
            onClick={handleReset}
            className="px-4 py-2 bg-gradient-to-r from-teal-500 to-purple-500 text-white rounded-lg hover:from-teal-600 hover:to-purple-600 transition-all font-medium"
          >
            Try Another Image
          </button>
        </motion.div>
      )}

      {!hasResults && (
        <>
          <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            className={`relative border-2 border-dashed rounded-2xl p-12 transition-all ${
              isDragging
                ? 'border-teal-500 bg-teal-500/10'
                : 'border-slate-700 bg-slate-800/50'
            }`}
          >
            <input
              type="file"
              id="file-upload"
              accept="image/*"
              onChange={handleFileInput}
              className="hidden"
            />
            
            {previewUrl ? (
              <div className="text-center">
                <motion.img
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  src={previewUrl}
                  alt="Preview"
                  className="max-h-64 mx-auto rounded-lg shadow-lg mb-4"
                />
                <p className="text-slate-300 font-medium mb-2">{selectedFile?.name}</p>
                <div className="flex gap-3 justify-center">
                  <button
                    onClick={handleSubmit}
                    className="px-6 py-3 bg-gradient-to-r from-teal-500 to-purple-500 text-white rounded-lg hover:from-teal-600 hover:to-purple-600 transition-all shadow-lg hover:shadow-xl font-semibold"
                  >
                    Find Similar Images
                  </button>
                  <button
                    onClick={handleReset}
                    className="px-6 py-3 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition-all font-medium"
                  >
                    Change Image
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center">
                <div className="mb-4">
                  <svg
                    className="mx-auto h-16 w-16 text-slate-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                    />
                  </svg>
                </div>
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer inline-flex items-center px-6 py-3 bg-gradient-to-r from-teal-500 to-purple-500 text-white rounded-lg hover:from-teal-600 hover:to-purple-600 transition-all shadow-lg hover:shadow-xl font-semibold"
                >
                  Choose Image
                </label>
                <p className="text-slate-400 mt-4">or drag and drop an image here</p>
              </div>
            )}
          </div>

          <p className="text-center text-slate-300 text-lg mt-6 mb-4">
            Find visually similar items from our catalog
          </p>

          <div>
            <p className="text-slate-400 text-sm text-center mb-3">Or try a sample:</p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {SAMPLE_IMAGES.map((sample, index) => (
                <motion.button
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  onClick={() => handleSampleClick(sample.path)}
                  className="group relative aspect-square rounded-xl overflow-hidden border-2 border-slate-700 hover:border-teal-500 transition-all shadow-lg hover:shadow-teal-500/30"
                >
                  <img
                    src={sample.path}
                    alt={sample.name}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent flex items-end p-3">
                    <span className="text-white text-sm font-medium">{sample.name}</span>
                  </div>
                </motion.button>
              ))}
            </div>
          </div>
        </>
      )}
    </motion.div>
  );
};

export default UploadSection;
