import axios from 'axios';

// Interface with ID
interface Review {
    id: string;
    product_id: string;
    rating: number;
    comment: string;
}

// Interface without ID (for creating new reviews)
interface ReviewInput {
    product_id: string;
    rating: number;
    comment: string;
}

// Get all reviews
export async function getAllReviews(): Promise<Review[]> {
    try {
        const response = await axios.get('http://127.0.0.1:8000/reviews/all');
        return response.data;
    } catch (error) {
        console.error('Error fetching all reviews:', error);
        throw error;
    }
}

// Get reviews for specific product
export async function getReviewsByProductId(productId: string): Promise<Review[]> {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/reviews/product/${productId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching reviews for product ID ${productId}:`, error);
        throw error;
    }
}

// Get review by ID
export async function getReviewById(reviewId: string): Promise<Review> {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/reviews/${reviewId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching review ID ${reviewId}:`, error);
        throw error;
    }
}

// Create new review
export async function createReview(reviewData: ReviewInput): Promise<Review> {
    try {
        const response = await axios.post('http://127.0.0.1:8000/reviews/', reviewData);
        return response.data;
    } catch (error) {
        console.error('Error creating review:', error);
        throw error;
    }
}

// Update review
export async function updateReview(reviewId: string, reviewData: ReviewInput): Promise<Review> {
    try {
        const response = await axios.put(`http://127.0.0.1:8000/reviews/${reviewId}`, reviewData);
        return response.data;
    } catch (error) {
        console.error(`Error updating review ID ${reviewId}:`, error);
        throw error;
    }
}

// Delete review
export async function deleteReview(reviewId: string): Promise<void> {
    try {
        await axios.delete(`http://127.0.0.1:8000/reviews/${reviewId}`);
    } catch (error) {
        console.error(`Error deleting review ID ${reviewId}:`, error);
        throw error;
    }
}