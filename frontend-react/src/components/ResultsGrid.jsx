import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import ResultCard from './ResultCard';

const ResultsGrid = ({ images, loading }) => {
  const resultsRef = useRef(null);

  useEffect(() => {
    if (images.length > 0 && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }, [images]);

  const calculateAverageSimilarity = () => {
    if (images.length === 0) return 0;
    const sum = images.reduce((acc, img) => acc + img.similarity, 0);
    return sum / images.length;
  };

  const avgSimilarity = calculateAverageSimilarity();
  const bestSimilarity = images.length > 0 ? Math.max(...images.map(img => img.similarity)) : 0;

  const getConfidenceState = () => {
    const threshold = Math.max(avgSimilarity, bestSimilarity);
    if (threshold >= 0.75) return 'success';
    if (threshold >= 0.6) return 'warning';
    return 'poor';
  };

  const confidenceState = getConfidenceState();

  if (loading) {
    return (
      <div ref={resultsRef} className="mt-12">
        <div className="flex flex-col items-center justify-center py-16">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-teal-500/20 border-t-teal-500 rounded-full animate-spin" />
          </div>
          <p className="text-slate-400 mt-4 text-lg">Finding similar images...</p>
        </div>
      </div>
    );
  }

  if (images.length === 0) {
    return null;
  }

  return (
    <div ref={resultsRef} className="mt-12 max-w-7xl mx-auto px-4">
      {confidenceState === 'success' && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 bg-gradient-to-r from-teal-500/10 to-purple-500/10 border border-teal-500/30 rounded-xl p-4"
        >
          <h2 className="text-xl font-bold text-white mb-1">
            Found {images.length} similar images
          </h2>
          <p className="text-teal-400">
            Average similarity: {(avgSimilarity * 100).toFixed(0)}% · Best match: {(bestSimilarity * 100).toFixed(0)}%
          </p>
        </motion.div>
      )}

      {confidenceState === 'warning' && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-4"
        >
          <h2 className="text-xl font-bold text-yellow-400 mb-1">
            ⚠️ Limited matches found
          </h2>
          <p className="text-yellow-300">
            This image might not belong to our catalog. Results may be less accurate.
          </p>
          <p className="text-slate-400 text-sm mt-1">
            Average similarity: {(avgSimilarity * 100).toFixed(0)}%
          </p>
        </motion.div>
      )}

      {confidenceState === 'poor' ? (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-slate-800 rounded-2xl p-8 text-center border border-slate-700"
        >
          <div className="text-6xl mb-4">🔍</div>
          <h3 className="text-2xl font-bold text-white mb-2">No relevant matches found</h3>
          <p className="text-slate-400 mb-4">
            Try uploading a product image similar to our catalog.
          </p>
          <p className="text-slate-500 text-sm">
            Best similarity score: {(bestSimilarity * 100).toFixed(0)}%
          </p>
        </motion.div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {images.map((image, index) => (
            <ResultCard key={image.id || index} image={image} index={index} />
          ))}
        </div>
      )}
    </div>
  );
};

export default ResultsGrid;
