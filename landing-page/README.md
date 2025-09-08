# PathWise Landing Page

A modern, responsive landing page for PathWise - an AI-powered personalized learning platform.

## Features

### 🎨 Modern Design
- Clean, professional design with modern UI/UX principles
- Gradient backgrounds and glassmorphism effects
- Responsive design that works on all devices
- Smooth animations and transitions

### 🚀 Key Sections
- **Hero Section**: Compelling value proposition with clear CTAs
- **Statistics**: Key metrics showcasing platform success
- **Features**: Six key features highlighting AI-powered learning
- **How It Works**: Simple 3-step process explanation
- **Call to Action**: Final conversion section
- **Footer**: Comprehensive links and social media

### 🔐 Authentication Pages
- **Login Page**: Clean, secure login with social auth options
- **Registration Page**: Comprehensive signup with password strength indicator
- Form validation and error handling
- Social authentication integration ready

## Technology Stack

- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern CSS with custom properties (CSS variables)
- **Bootstrap 5**: Responsive grid and components
- **Font Awesome**: Icon library for consistent iconography
- **Google Fonts**: Inter and Poppins for modern typography
- **Vanilla JavaScript**: No external dependencies for core functionality

## File Structure

```
landing-page/
├── index.html          # Main landing page
├── login.html          # Login page
├── register.html       # Registration page
├── README.md          # This file
└── assets/            # (Optional) Additional assets
    ├── images/        # Images and graphics
    ├── css/          # Additional CSS files
    └── js/           # Additional JavaScript files
```

## Key Features

### 🎯 Landing Page (index.html)
- Hero section with animated background
- Statistics counter animation
- Feature cards with hover effects
- Smooth scroll navigation
- Responsive mobile design

### 🔑 Login Page (login.html)
- Modern glassmorphism design
- Form validation with real-time feedback
- Social authentication buttons
- Loading states and error handling
- Password strength indicators

### 📝 Registration Page (register.html)
- Multi-step form validation
- Password strength meter
- Terms and conditions checkbox
- Comprehensive error handling
- Social registration options

## Integration Points

### Backend API Endpoints
The pages are configured to work with these API endpoints:

- `POST /auth/login` - User authentication
- `POST /auth/register` - User registration
- `GET /auth/{provider}` - Social authentication (Google, LinkedIn, GitHub, Facebook)

### Dashboard Integration
- Successful authentication redirects to `http://localhost:5173/dashboard`
- Token storage in localStorage for session management

## Customization

### Color Scheme
The design uses CSS custom properties for easy theming:

```css
:root {
    --primary-color: #6366f1;      /* Indigo */
    --secondary-color: #10b981;     /* Emerald */
    --accent-color: #f59e0b;        /* Amber */
    --text-dark: #1f2937;           /* Dark gray */
    --text-light: #6b7280;          /* Light gray */
}
```

### Typography
- **Primary Font**: Inter (clean, modern sans-serif)
- **Display Font**: Poppins (for headings and branding)

### Responsive Breakpoints
- Mobile: < 480px
- Tablet: 481px - 768px
- Desktop: > 768px

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

- Optimized images and assets
- Minimal external dependencies
- Efficient CSS with modern features
- Lazy loading for better performance

## Accessibility

- Semantic HTML structure
- ARIA labels where appropriate
- Keyboard navigation support
- High contrast color ratios
- Screen reader friendly

## Getting Started

1. Open `index.html` in a web browser
2. For development, use a local server:
   ```bash
   # Using Python
   python -m http.server 8080
   
   # Using Node.js
   npx serve .
   
   # Using Live Server (VS Code extension)
   Right-click index.html → "Open with Live Server"
   ```

## Deployment

The landing page is static and can be deployed to any web hosting service:

- **Netlify**: Drag and drop the folder
- **Vercel**: Connect to Git repository
- **GitHub Pages**: Push to gh-pages branch
- **Traditional hosting**: Upload files via FTP

## Future Enhancements

- [ ] Add more interactive animations
- [ ] Implement A/B testing for different CTAs
- [ ] Add testimonials carousel
- [ ] Include pricing section
- [ ] Add blog integration
- [ ] Implement newsletter signup
- [ ] Add chatbot integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test across different browsers and devices
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**PathWise** - Empowering learners worldwide with AI-powered personalized education.
