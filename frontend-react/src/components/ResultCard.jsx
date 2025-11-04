import React, { useState } from 'react';
import { motion } from 'framer-motion';

const ResultCard = ({ image, index }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="relative group"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="bg-slate-800 rounded-2xl overflow-hidden shadow-lg transition-all duration-300 hover:shadow-2xl hover:shadow-teal-500/20">
        <div className="relative aspect-square overflow-hidden">
          <motion.img
            src={image.url || image.thumbnail}
            alt={image.name || `Similar image ${index + 1}`}
            className="w-full h-full object-cover"
            animate={{ scale: isHovered ? 1.1 : 1 }}
            transition={{ duration: 0.3 }}
          />
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: isHovered ? 1 : 0 }}
            className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent flex items-center justify-center"
          >
            <span className="text-white font-semibold text-lg">View Details</span>
          </motion.div>
        </div>
        
        <div className="p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-400 text-sm font-medium">Similarity</span>
            <div className="flex items-center gap-2">
              <div className="bg-gradient-to-r from-teal-500 to-purple-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                {(image.similarity * 100).toFixed(0)}%
              </div>
            </div>
          </div>
          
          {image.name && (
            <p className="text-slate-300 text-sm truncate" title={image.name}>
              {image.name}
            </p>
          )}
          
          <div className="mt-2 bg-slate-700 rounded-full h-2 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${image.similarity * 100}%` }}
              transition={{ delay: index * 0.1 + 0.3, duration: 0.6 }}
              className="h-full bg-gradient-to-r from-teal-500 to-purple-500"
            />
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default ResultCard;
