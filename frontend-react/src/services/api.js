const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const uploadImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);

  try {
    const response = await fetch(`${API_BASE_URL}/api/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Upload failed');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error uploading image:', error);
    throw error;
  }
};

export const getSimilarImages = async (imageId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/similar/${imageId}`);

    if (!response.ok) {
      throw new Error('Failed to fetch similar images');
    }

    const data = await response.json();
    return data.similar_images || [];
  } catch (error) {
    console.error('Error fetching similar images:', error);
    throw error;
  }
};

export const uploadAndGetSimilar = async (imageFile) => {
  try {
    const uploadResult = await uploadImage(imageFile);
    const similarImages = await getSimilarImages(uploadResult.image_id);
    return similarImages;
  } catch (error) {
    console.error('Error in uploadAndGetSimilar:', error);
    throw error;
  }
};
