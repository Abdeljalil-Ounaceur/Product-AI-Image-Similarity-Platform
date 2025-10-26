import React from 'react';

const ImageItem = ({ image, rank }) => {
  return (
    <div className="image-item">
      <div className="rank-badge">{rank}</div>
      <img 
        src={image.url || image.thumbnail} 
        alt={image.name || `Similar image ${rank}`}
        className="item-image"
      />
      <div className="item-info">
        <div className="similarity-score">
          {image.similarity ? `${(image.similarity * 100).toFixed(1)}% match` : 'N/A'}
        </div>
        {image.name && <div className="item-name">{image.name}</div>}
      </div>
    </div>
  );
};

export default ImageItem;
