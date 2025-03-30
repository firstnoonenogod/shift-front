import axios  from "axios";

interface Category {
    id: string;
    name: string;
    description: string;
}
interface CategoryInput {
    name: string;
    description: string;
}

export async function getCategory(): Promise<Category[]> {
    try {
        const response = await axios.get('http://127.0.0.1:8000/categories/');
        return response.data
    }
    catch (error) {
        console.error("error categoires : ", error);
        throw error;
        
    }
}

// Function to get category by ID
export async function getCategoryById(id: string): Promise<Category> {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/categories/${id}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching category with ID ${id}:`, error);
        throw error;
    }
}

// Function to update category
export async function updateCategory(id: string, categoryData: CategoryInput): Promise<Category> {
    try {
        const response = await axios.put(`http://127.0.0.1:8000/categories/${id}`, categoryData);
        return response.data;
    } catch (error) {
        console.error(`Error updating category with ID ${id}:`, error);
        throw error;
    }
}

// Function to delete category
export async function deleteCategory(id: string): Promise<void> {
    try {
        await axios.delete(`http://127.0.0.1:8000/categories/${id}`);
    } catch (error) {
        console.error(`Error deleting category with ID ${id}:`, error);
        throw error;
    }
}

// Function to create a new category
export async function createCategory(categoryData: CategoryInput): Promise<Category> {
    try {
        const response = await axios.post('http://127.0.0.1:8000/categories/', categoryData);
        return response.data;
    } catch (error) {
        console.error('Error creating category:', error);
        throw error;
    }
}