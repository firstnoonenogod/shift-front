import axios from "axios";

// Interface with ID
interface Variant {
    id: string;
    size: string;
    color: string;
    product_id: string;
    price: number;
    stock: number;
}

// Interface without ID (for creating new variants)
interface VariantInput {
    size: string;
    color: string;
    product_id: string;
    price: number;
    stock: number;
}

// Function to get all variants
export async function getVariants(): Promise<Variant[]> {
    try {
        const response = await axios.get('http://127.0.0.1:8000/variants/');
        return response.data;
    } catch (error) {
        console.error('Error fetching variants:', error);
        throw error;
    }
}

// Function to get variant by ID
export async function getVariantById(id: string): Promise<Variant> {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/variants/${id}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching variant with ID ${id}:`, error);
        throw error;
    }
}

// Function to create a new variant
export async function createVariant(variantData: VariantInput): Promise<Variant> {
    try {
        const response = await axios.post('http://127.0.0.1:8000/variants/', variantData);
        return response.data;
    } catch (error) {
        console.error('Error creating variant:', error);
        throw error;
    }
}

// Function to update variant
export async function updateVariant(id: string, variantData: VariantInput): Promise<Variant> {
    try {
        const response = await axios.put(`http://127.0.0.1:8000/variants/${id}`, variantData);
        return response.data;
    } catch (error) {
        console.error(`Error updating variant with ID ${id}:`, error);
        throw error;
    }
}

// Function to delete variant
export async function deleteVariant(id: string): Promise<void> {
    try {
        await axios.delete(`http://127.0.0.1:8000/variants/${id}`);
    } catch (error) {
        console.error(`Error deleting variant with ID ${id}:`, error);
        throw error;
    }
}

// Function to get variants by product ID
export async function getVariantsByProductId(productId: string): Promise<Variant[]> {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/variants/product/${productId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching variants for product ID ${productId}:`, error);
        throw error;
    }
}