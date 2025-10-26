import React from 'react';
import ImageItem from './ImageItem';

const ImageList = ({ images, loading }) => {
  if (loading) {
    return (
      <div className="image-list">
        <h2>Similar Images</h2>
        <div className="loading">Loading...</div>
      </div>
    );
  }

  if (!images || images.length === 0) {
    return (
      <div className="image-list">
        <h2>Similar Images</h2>
        <div className="empty-state">
          Upload an image to find similar ones
        </div>
      </div>
    );
  }

  return (
    <div className="image-list">
      <h2>Similar Images</h2>
      <div className="images-grid">
        {images.map((image, index) => (
          <ImageItem 
            key={image.id || index} 
            image={image} 
            rank={index + 1}
          />
        ))}
      </div>
    </div>
  );
};

export default ImageList;
