const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Upload an image to the backend for processing
 * 
 * @endpoint POST /api/upload
 * 
 * @request
 * Content-Type: multipart/form-data
 * Body: {
 *   image: File  // Image file (jpg, png, etc.)
 * }
 * 
 * @response
 * Content-Type: application/json
 * Success (200): {
 *   image_id: string,      // Unique identifier for the uploaded image
 *   message?: string,      // Optional success message
 *   filename?: string      // Original filename
 * }
 * 
 * Error (4xx/5xx): {
 *   detail?: string,       // Error message
 *   error?: string         // Alternative error message field
 * }
 * 
 * @param {File} imageFile - The image file to upload
 * @returns {Promise<{image_id: string, message?: string, filename?: string}>}
 * @throws {Error} When upload fails
 */
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

/**
 * Get similar images for a given image ID
 * 
 * @endpoint GET /api/similar/{imageId}
 * 
 * @request
 * Method: GET
 * URL Parameters: {
 *   imageId: string  // The unique identifier of the uploaded image
 * }
 * 
 * @response
 * Content-Type: application/json
 * Success (200): {
 *   similar_images: Array<{
 *     image_id: string,           // ID of the similar image
 *     similarity_score: number,   // Similarity score (0-1 or 0-100)
 *     url?: string,               // URL to access the image
 *     filename?: string,          // Filename of the similar image
 *     metadata?: object           // Additional metadata
 *   }>
 * }
 * 
 * Error (4xx/5xx): {
 *   detail?: string,              // Error message
 *   error?: string                // Alternative error message field
 * }
 * 
 * @param {string} imageId - The unique identifier of the uploaded image
 * @returns {Promise<Array<{image_id: string, similarity_score: number, url?: string, filename?: string, metadata?: object}>>}
 * @throws {Error} When fetching similar images fails
 */
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
