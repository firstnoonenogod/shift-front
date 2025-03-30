/**
 * Provides a data URL for a placeholder image when remote placeholder services are not available
 * @param {number} width - Width of the placeholder
 * @param {number} height - Height of the placeholder (defaults to width if not provided)
 * @param {string} text - Optional text to display on the placeholder
 * @param {string} bgColor - Background color in hex format
 * @param {string} textColor - Text color in hex format
 * @returns {string} - Data URL for the placeholder image
 */
export function getPlaceholder(width = 100, height = null, text = '', bgColor = '#e2e2e2', textColor = '#999999') {
    if (typeof document === 'undefined') {
        // SSR environment, return a simple data URL
        return 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiB2aWV3Qm94PSIwIDAgMjAwIDIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNlMmUyZTIiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9Im1vbm9zcGFjZSIgZm9udC1zaXplPSIyNnB4IiBmaWxsPSIjOTk5OTk5Ij5ObyBJbWFnZTwvdGV4dD48L3N2Zz4=';
    }
    height = height || width;
    // Create a canvas element
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');

    // Draw background
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, width, height);

    // Draw text if provided
    if (text) {
        ctx.fillStyle = textColor;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        // Scale font size based on canvas size
        const fontSize = Math.min(width, height) * 0.2;
        ctx.font = `bold ${fontSize}px Arial, sans-serif`;
        ctx.fillText(text, width / 2, height / 2);
    }

    // Convert canvas to data URL
    return canvas.toDataURL('image/png');
}

/**
 * Get initials from a username or email
 * @param {string} name - Name or email to extract initials from
 * @returns {string} - Extracted initials (1-2 characters)
 */
export function getInitials(name) {
    if (!name) return '?';

    // For an email address, take the first character
    if (name.includes('@')) {
        return name.split('@')[0][0].toUpperCase();
    }

    // For a name, take first letter of each word (max 2)
    const parts = name.trim().split(/\s+/);
    if (parts.length === 1) {
        return parts[0][0].toUpperCase();
    }
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

/**
 * Creates an avatar with a colored background
 * @param {string} name - Name to extract initial from or initials to display
 * @param {number} size - Size of the avatar in pixels
 * @param {string} bgColor - Background color (optional)
 * @returns {string} - Data URL for the avatar image
 */
export function getAvatarPlaceholder(name = 'User', size = 100, bgColor = null) {
    // Check if window is defined (for SSR compatibility)
    if (typeof window === 'undefined') {
        return `data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMCAwIDQwIDQwIj48cmVjdCB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIGZpbGw9IiNlZTRkMmQiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9Im1vbm9zcGFjZSIgZm9udC1zaXplPSIyMHB4IiBmaWxsPSIjZmZmZmZmIj4/PC90ZXh0Pjwvc3ZnPg==`;
    }

    try {
        // Get initials if a full name is provided
        const initials = name.length > 2 ? getInitials(name) : name;
        
        // Generate a consistent color based on the name if bgColor not provided
        if (!bgColor) {
            // Simple hash function to generate a color
            let hash = 0;
            for (let i = 0; i < name.length; i++) {
                hash = name.charCodeAt(i) + ((hash << 5) - hash);
            }
            // Convert hash to RGB color
            const h = Math.abs(hash) % 360;
            bgColor = `hsl(${h}, 70%, 50%)`;
        }

        // Create a canvas element
        const canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d');

        // Draw background
        ctx.fillStyle = bgColor;
        ctx.fillRect(0, 0, size, size);

        // Draw text
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.font = `bold ${size * 0.5}px Arial, sans-serif`;
        ctx.fillText(initials, size / 2, size / 2);

        // Convert canvas to data URL
        return canvas.toDataURL('image/png');
    } catch (error) {
        console.error('Error generating avatar placeholder:', error);
        return `data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMCAwIDQwIDQwIj48cmVjdCB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIGZpbGw9IiNlZTRkMmQiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9Im1vbm9zcGFjZSIgZm9udC1zaXplPSIyMHB4IiBmaWxsPSIjZmZmZmZmIj4/PC90ZXh0Pjwvc3ZnPg==`;
    }
}

/**
 * Generate a placeholder image when product images are not available
 * @param {number} width - Width of the placeholder
 * @param {number} height - Height of the placeholder
 * @param {string} text - Text to display on the placeholder
 * @returns {string} - Data URL of the generated placeholder image
 */
export function getProductPlaceholder(width = 300, height = 300, text = 'No Image') {
    // Check if window is defined (for SSR compatibility)
    if (typeof window === 'undefined') {
        return `data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiB2aWV3Qm94PSIwIDAgMjAwIDIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNmOGY5ZmEiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9Im1vbm9zcGFjZSIgZm9udC1zaXplPSIyNnB4IiBmaWxsPSIjZGRkZGRkIj5ObyBJbWFnZTwvdGV4dD48L3N2Zz4=`;
    }

    try {
        // Create canvas element
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');

        // Background
        ctx.fillStyle = '#f8f9fa';
        ctx.fillRect(0, 0, width, height);

        // Shirt icon (simplified)
        ctx.fillStyle = '#eeeeee';
        ctx.beginPath();
        // Draw a simple shirt shape
        const x = width / 2;
        const y = height / 2 - 20;
        const shirtWidth = width * 0.4;
        ctx.moveTo(x - shirtWidth/2, y - shirtWidth/3);
        ctx.lineTo(x + shirtWidth/2, y - shirtWidth/3);
        ctx.lineTo(x + shirtWidth/2, y + shirtWidth/2);
        ctx.lineTo(x + shirtWidth/4, y + shirtWidth/1.5);
        ctx.lineTo(x - shirtWidth/4, y + shirtWidth/1.5);
        ctx.lineTo(x - shirtWidth/2, y + shirtWidth/2);
        ctx.closePath();
        ctx.fill();

        // Line in the middle of the shirt
        ctx.strokeStyle = '#e0e0e0';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x, y - shirtWidth/3);
        ctx.lineTo(x, y + shirtWidth/5);
        ctx.stroke();

        // Collar
        ctx.beginPath();
        ctx.arc(x - shirtWidth/6, y - shirtWidth/3, shirtWidth/8, 0, Math.PI, true);
        ctx.arc(x + shirtWidth/6, y - shirtWidth/3, shirtWidth/8, 0, Math.PI, true);
        ctx.fillStyle = '#f8f9fa';
        ctx.fill();

        // Text
        ctx.fillStyle = '#cccccc';
        ctx.font = `bold ${width * 0.08}px Arial, sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(text, width/2, height * 0.75);

        // Return data URL
        return canvas.toDataURL('image/png');
    } catch (error) {
        console.error('Error generating placeholder image:', error);
        return 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiB2aWV3Qm94PSIwIDAgMjAwIDIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNmOGY5ZmEiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9Im1vbm9zcGFjZSIgZm9udC1zaXplPSIyNnB4IiBmaWxsPSIjZGRkZGRkIj5ObyBJbWFnZTwvdGV4dD48L3N2Zz4=';
    }
}
