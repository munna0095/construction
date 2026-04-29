import React, { useState, useEffect, useRef } from 'https://esm.sh/react@18.2.0';

// ============================================================
// SIDDHI CONSTRUCTION WEBSITE - REACT COMPONENT
// ============================================================
// Complete 7-page construction website with 3D animation
// Built with React, Three.js, Tailwind CSS, and GSAP
// ============================================================

// 3D Hero Background Component
const ThreeDHeroBackground = () => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Dynamically import Three.js
    import('https://cdn.jsdelivr.net/npm/three@r128/build/three.module.js').then((THREE) => {
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
      
      renderer.setSize(window.innerWidth, window.innerHeight * 0.6);
      renderer.setClearColor(0x000000, 0.1);
      containerRef.current.appendChild(renderer.domElement);

      // Create rotating shapes
      const geometry1 = new THREE.BoxGeometry(2, 2, 2);
      const material1 = new THREE.MeshPhongMaterial({ color: 0xFF6B35, wireframe: false });
      const cube = new THREE.Mesh(geometry1, material1);
      scene.add(cube);

      const geometry2 = new THREE.OctahedronGeometry(1.5);
      const material2 = new THREE.MeshPhongMaterial({ color: 0xFFC72C });
      const octahedron = new THREE.Mesh(geometry2, material2);
      octahedron.position.x = -4;
      scene.add(octahedron);

      const geometry3 = new THREE.TetrahedronGeometry(1.5);
      const material3 = new THREE.MeshPhongMaterial({ color: 0xFF6B35 });
      const tetrahedron = new THREE.Mesh(geometry3, material3);
      tetrahedron.position.x = 4;
      scene.add(tetrahedron);

      // Lighting
      const light = new THREE.PointLight(0xffffff, 1);
      light.position.set(5, 5, 5);
      scene.add(light);

      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      scene.add(ambientLight);

      camera.position.z = 8;

      const animate = () => {
        requestAnimationFrame(animate);
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;
        octahedron.rotation.x -= 0.005;
        octahedron.rotation.y -= 0.008;
        tetrahedron.rotation.x += 0.008;
        tetrahedron.rotation.y -= 0.01;
        renderer.render(scene, camera);
      };

      animate();

      const handleResize = () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight * 0.6);
      };

      window.addEventListener('resize', handleResize);
      return () => {
        window.removeEventListener('resize', handleResize);
        containerRef.current?.removeChild(renderer.domElement);
      };
    });
  }, []);

  return <div ref={containerRef} style={{ width: '100%', height: '60vh' }} />;
};

// Navigation Component
const Navigation = ({ currentPage, setCurrentPage }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const pages = ['Home', 'Projects', 'Services', 'About', 'Team', 'Gallery', 'Contact'];

  return (
    <nav className="bg-gradient-to-r from-gray-900 to-gray-800 sticky top-0 z-50 glass">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          <div className="flex items-center">
            <h1 
              onClick={() => setCurrentPage('Home')}
              className="text-3xl font-bold gradient-text cursor-pointer"
            >
              🏗️ SIDDHI
            </h1>
          </div>
          
          {/* Desktop Menu */}
          <div className="hidden md:flex space-x-8">
            {pages.map(page => (
              <button
                key={page}
                onClick={() => setCurrentPage(page)}
                className={`px-3 py-2 text-sm font-medium transition-all ${
                  currentPage === page
                    ? 'text-orange-500 border-b-2 border-orange-500'
                    : 'text-gray-300 hover:text-orange-500'
                }`}
              >
                {page}
              </button>
            ))}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-orange-500"
          >
            ☰
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 space-y-2">
            {pages.map(page => (
              <button
                key={page}
                onClick={() => {
                  setCurrentPage(page);
                  setMobileMenuOpen(false);
                }}
                className={`block w-full text-left px-3 py-2 text-sm font-medium ${
                  currentPage === page ? 'text-orange-500' : 'text-gray-300'
                }`}
              >
                {page}
              </button>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
};

// Home Page
const HomePage = () => (
  <div className="min-h-screen construction-pattern">
    <ThreeDHeroBackground />
    
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div className="text-center mb-20 animate-fade-in">
        <h2 className="text-5xl md:text-6xl font-bold mb-6">
          <span className="gradient-text">Building Excellence</span>
        </h2>
        <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
          SIDDHI CONSTRUCTION - Where quality meets innovation. Building dreams into reality for over a decade.
        </p>
        <button className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-lg font-bold text-lg transition-all hover:scale-105 glow-orange">
          Get Started
        </button>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
        {[
          { icon: '🏢', title: '50+ Projects', desc: 'Successfully completed' },
          { icon: '👥', title: '100+ Team', desc: 'Expert professionals' },
          { icon: '⭐', title: '10+ Years', desc: 'Industry experience' }
        ].map((feature, i) => (
          <div key={i} className="glass p-8 rounded-lg hover-lift transition-all">
            <div className="text-5xl mb-4">{feature.icon}</div>
            <h3 className="text-2xl font-bold mb-2">{feature.title}</h3>
            <p className="text-gray-400">{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
  </div>
);

// Projects Page
const ProjectsPage = () => {
  const [selectedProject, setSelectedProject] = useState(null);

  const projects = [
    { id: 1, name: 'Luxury Residential Complex', location: 'Pune', category: 'Residential', area: '50,000 sq ft', timeline: '2023-2024', desc: 'Premium residential project with 100+ units', image: '🏢', status: 'Completed' },
    { id: 2, name: 'Tech Park', location: 'Bangalore', category: 'Commercial', area: '100,000 sq ft', timeline: '2024-2025', desc: 'State-of-the-art tech park facility', image: '🏗️', status: 'Ongoing' },
    { id: 3, name: 'Hospital Building', location: 'Mumbai', category: 'Infrastructure', area: '75,000 sq ft', timeline: '2023-2024', desc: 'Multi-specialty hospital complex', image: '🏥', status: 'Completed' },
    { id: 4, name: 'Shopping Mall', location: 'Delhi', category: 'Commercial', area: '150,000 sq ft', timeline: '2024-2026', desc: 'Modern shopping and entertainment hub', image: '🛍️', status: 'Ongoing' },
    { id: 5, name: 'School Campus', location: 'Hyderabad', category: 'Residential', area: '80,000 sq ft', timeline: '2023-2024', desc: 'Educational institution with modern facilities', image: '🎓', status: 'Completed' },
    { id: 6, name: 'Software Office', location: 'Pune', category: 'Commercial', area: '60,000 sq ft', timeline: '2024-2025', desc: 'Corporate office space with eco-friendly design', image: '💼', status: 'Ongoing' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black py-20 construction-pattern">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-5xl font-bold text-center mb-4 gradient-text">Our Projects</h2>
        <p className="text-center text-gray-400 mb-12">Showcase of our finest work across residential, commercial, and infrastructure</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {projects.map(project => (
            <div
              key={project.id}
              onClick={() => setSelectedProject(project)}
              className="glass p-6 rounded-lg hover-lift cursor-pointer transition-all"
            >
              <div className="text-6xl mb-4">{project.image}</div>
              <h3 className="text-2xl font-bold mb-2">{project.name}</h3>
              <p className="text-gray-400 mb-4">{project.location}</p>
              <div className="flex justify-between items-center">
                <span className={`px-3 py-1 rounded text-sm font-bold ${project.status === 'Completed' ? 'bg-green-900 text-green-200' : 'bg-orange-900 text-orange-200'}`}>
                  {project.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Project Detail Modal */}
      {selectedProject && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4" onClick={() => setSelectedProject(null)}>
          <div className="bg-gray-900 rounded-lg p-8 max-w-2xl w-full" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-4xl font-bold mb-2">{selectedProject.name}</h2>
                <p className="text-gray-400">{selectedProject.location}</p>
              </div>
              <button onClick={() => setSelectedProject(null)} className="text-2xl">✕</button>
            </div>
            
            <div className="text-6xl mb-6">{selectedProject.image}</div>
            
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="glass p-4 rounded">
                <p className="text-gray-400">Category</p>
                <p className="text-xl font-bold">{selectedProject.category}</p>
              </div>
              <div className="glass p-4 rounded">
                <p className="text-gray-400">Area</p>
                <p className="text-xl font-bold">{selectedProject.area}</p>
              </div>
              <div className="glass p-4 rounded">
                <p className="text-gray-400">Timeline</p>
                <p className="text-xl font-bold">{selectedProject.timeline}</p>
              </div>
              <div className="glass p-4 rounded">
                <p className="text-gray-400">Status</p>
                <p className="text-xl font-bold text-orange-500">{selectedProject.status}</p>
              </div>
            </div>
            
            <p className="text-gray-300 mb-6">{selectedProject.desc}</p>
            <button onClick={() => setSelectedProject(null)} className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-lg font-bold">
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

// Services Page
const ServicesPage = () => {
  const services = [
    { icon: '🏡', title: 'Residential', desc: 'Luxury homes and apartments' },
    { icon: '🏢', title: 'Commercial', desc: 'Office buildings and complexes' },
    { icon: '🌉', title: 'Infrastructure', desc: 'Roads, bridges, utilities' },
    { icon: '🎨', title: 'Interior Design', desc: 'Creative interior solutions' },
    { icon: '🔧', title: 'Renovation', desc: 'Modern renovation services' },
    { icon: '📋', title: 'Consulting', desc: 'Project planning & consulting' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black py-20 construction-pattern">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-5xl font-bold text-center mb-4 gradient-text">Our Services</h2>
        <p className="text-center text-gray-400 mb-12">Comprehensive construction solutions for all your needs</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, i) => (
            <div key={i} className="glass p-8 rounded-lg hover-lift">
              <div className="text-6xl mb-4">{service.icon}</div>
              <h3 className="text-2xl font-bold mb-2">{service.title}</h3>
              <p className="text-gray-400">{service.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// About Page
const AboutPage = () => (
  <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black py-20 construction-pattern">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 className="text-5xl font-bold mb-12 gradient-text">About SIDDHI</h2>
      
      <div className="glass p-8 rounded-lg mb-12">
        <p className="text-xl text-gray-300 leading-relaxed mb-6">
          SIDDHI CONSTRUCTION has been building dreams for over a decade. With a team of experts and a commitment to excellence, we deliver world-class construction projects across residential, commercial, and infrastructure sectors.
        </p>
        <p className="text-xl text-gray-300 leading-relaxed">
          Our philosophy: Quality, Transparency, and Innovation. Every project is a testament to our dedication to creating spaces that inspire and endure.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="glass p-8 rounded-lg">
          <h3 className="text-2xl font-bold mb-4 text-orange-500">Our Mission</h3>
          <p className="text-gray-300">To deliver exceptional construction projects that exceed expectations and create lasting value.</p>
        </div>
        <div className="glass p-8 rounded-lg">
          <h3 className="text-2xl font-bold mb-4 text-yellow-500">Our Vision</h3>
          <p className="text-gray-300">To be the most trusted and innovative construction partner in India.</p>
        </div>
        <div className="glass p-8 rounded-lg">
          <h3 className="text-2xl font-bold mb-4 text-orange-500">Our Values</h3>
          <p className="text-gray-300">Integrity, Excellence, Innovation, and Customer Satisfaction.</p>
        </div>
      </div>

      <div className="mt-12">
        <h3 className="text-3xl font-bold mb-8">Certifications & Awards</h3>
        <div className="glass p-8 rounded-lg">
          <ul className="space-y-4 text-gray-300">
            <li>✓ ISO 9001:2015 Certified</li>
            <li>✓ Best Construction Company Award 2023</li>
            <li>✓ Green Building Certification</li>
            <li>✓ Safety Excellence Award</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
);

// Team Page
const TeamPage = () => {
  const team = [
    { id: 1, name: 'Founder & CEO', role: 'Visionary Leader', image: '👨‍💼' },
    { id: 2, name: 'Project Director', role: 'Project Management', image: '👨‍🔧' },
    { id: 3, name: 'Chief Architect', role: 'Design & Planning', image: '👨‍🏫' },
    { id: 4, name: 'Finance Head', role: 'Financial Management', image: '👨‍💻' },
    { id: 5, name: 'Operations Lead', role: 'Operations & Logistics', image: '👩‍💼' },
    { id: 6, name: 'Safety Officer', role: 'Quality & Safety', image: '👷' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black py-20 construction-pattern">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-5xl font-bold text-center mb-4 gradient-text">Our Team</h2>
        <p className="text-center text-gray-400 mb-12">Meet the experts behind SIDDHI CONSTRUCTION</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {team.map(member => (
            <div key={member.id} className="glass p-8 rounded-lg hover-lift text-center">
              <div className="text-7xl mb-4">{member.image}</div>
              <h3 className="text-2xl font-bold mb-2">{member.name}</h3>
              <p className="text-orange-500">{member.role}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Gallery Page
const GalleryPage = () => {
  const gallery = [
    { id: 1, image: '🏗️' }, { id: 2, image: '🏢' }, { id: 3, image: '🏠' },
    { id: 4, image: '🌉' }, { id: 5, image: '🏛️' }, { id: 6, image: '🏭' },
    { id: 7, image: '🏘️' }, { id: 8, image: '🏪' }, { id: 9, image: '🏫' },
    { id: 10, image: '🏥' }, { id: 11, image: '🏨' }, { id: 12, image: '🎪' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black py-20 construction-pattern">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-5xl font-bold text-center mb-12 gradient-text">Photo Gallery</h2>
        
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-12">
          {gallery.map(item => (
            <div key={item.id} className="glass p-8 rounded-lg hover-lift cursor-pointer flex items-center justify-center h-40">
              <div className="text-6xl">{item.image}</div>
            </div>
          ))}
        </div>

        <div className="glass p-8 rounded-lg">
          <h3 className="text-2xl font-bold mb-4">Upload Your Photos</h3>
          <p className="text-gray-400 mb-4">Replace emoji placeholders with your actual project photos when ready</p>
          <button className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-lg font-bold">
            Update Gallery
          </button>
        </div>
      </div>
    </div>
  );
};

// Contact Page
const ContactPage = () => {
  const [formData, setFormData] = useState({ name: '', email: '', phone: '', projectType: '', message: '' });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Thank you for contacting SIDDHI CONSTRUCTION! We will get back to you soon.');
    setFormData({ name: '', email: '', phone: '', projectType: '', message: '' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black py-20 construction-pattern">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-5xl font-bold text-center mb-12 gradient-text">Contact Us</h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Form */}
          <div className="glass p-8 rounded-lg">
            <h3 className="text-2xl font-bold mb-6">Get In Touch</h3>
            <form onSubmit={handleSubmit} className="space-y-6">
              <input
                type="text"
                name="name"
                placeholder="Your Name"
                value={formData.name}
                onChange={handleChange}
                className="w-full bg-gray-800 text-white px-4 py-3 rounded border border-gray-700 focus:border-orange-500 outline-none"
                required
              />
              <input
                type="email"
                name="email"
                placeholder="Your Email"
                value={formData.email}
                onChange={handleChange}
                className="w-full bg-gray-800 text-white px-4 py-3 rounded border border-gray-700 focus:border-orange-500 outline-none"
                required
              />
              <input
                type="tel"
                name="phone"
                placeholder="Your Phone"
                value={formData.phone}
                onChange={handleChange}
                className="w-full bg-gray-800 text-white px-4 py-3 rounded border border-gray-700 focus:border-orange-500 outline-none"
              />
              <select
                name="projectType"
                value={formData.projectType}
                onChange={handleChange}
                className="w-full bg-gray-800 text-white px-4 py-3 rounded border border-gray-700 focus:border-orange-500 outline-none"
              >
                <option value="">Select Project Type</option>
                <option value="Residential">Residential</option>
                <option value="Commercial">Commercial</option>
                <option value="Infrastructure">Infrastructure</option>
              </select>
              <textarea
                name="message"
                placeholder="Your Message"
                value={formData.message}
                onChange={handleChange}
                className="w-full bg-gray-800 text-white px-4 py-3 rounded border border-gray-700 focus:border-orange-500 outline-none h-32"
                required
              />
              <button type="submit" className="w-full bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-bold glow-orange">
                Send Message
              </button>
            </form>
          </div>

          {/* Contact Info */}
          <div>
            <div className="glass p-8 rounded-lg mb-6">
              <h3 className="text-2xl font-bold mb-4">Contact Information</h3>
              <div className="space-y-6">
                <div>
                  <p className="text-gray-400 mb-2">Phone</p>
                  <p className="text-xl font-bold">+91 9876543210</p>
                </div>
                <div>
                  <p className="text-gray-400 mb-2">Email</p>
                  <p className="text-xl font-bold">info@siddhiconstruction.com</p>
                </div>
                <div>
                  <p className="text-gray-400 mb-2">Location</p>
                  <p className="text-xl font-bold">Pune, Maharashtra, India</p>
                </div>
              </div>
            </div>

            <div className="glass p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-4">Working Hours</h3>
              <div className="space-y-2 text-gray-300">
                <p>Monday - Friday: 9:00 AM - 6:00 PM</p>
                <p>Saturday: 10:00 AM - 4:00 PM</p>
                <p>Sunday: Closed</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Footer Component
const Footer = () => (
  <footer className="bg-gray-900 border-t border-gray-800 py-12">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
        <div>
          <h4 className="text-xl font-bold mb-4">SIDDHI CONSTRUCTION</h4>
          <p className="text-gray-400">Building excellence since 2015</p>
        </div>
        <div>
          <h4 className="text-lg font-bold mb-4">Quick Links</h4>
          <ul className="space-y-2 text-gray-400">
            <li><a href="#" className="hover:text-orange-500">Home</a></li>
            <li><a href="#" className="hover:text-orange-500">Projects</a></li>
            <li><a href="#" className="hover:text-orange-500">Services</a></li>
          </ul>
        </div>
        <div>
          <h4 className="text-lg font-bold mb-4">Services</h4>
          <ul className="space-y-2 text-gray-400">
            <li><a href="#" className="hover:text-orange-500">Residential</a></li>
            <li><a href="#" className="hover:text-orange-500">Commercial</a></li>
            <li><a href="#" className="hover:text-orange-500">Infrastructure</a></li>
          </ul>
        </div>
        <div>
          <h4 className="text-lg font-bold mb-4">Contact</h4>
          <p className="text-gray-400">+91 9876543210</p>
          <p className="text-gray-400">info@siddhiconstruction.com</p>
        </div>
      </div>
      <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
        <p>&copy; 2026 SIDDHI CONSTRUCTION. All rights reserved.</p>
      </div>
    </div>
  </footer>
);

// Main App Component
export default function SiddhiConstructionWebsite() {
  const [currentPage, setCurrentPage] = useState('Home');

  const renderPage = () => {
    switch (currentPage) {
      case 'Home': return <HomePage />;
      case 'Projects': return <ProjectsPage />;
      case 'Services': return <ServicesPage />;
      case 'About': return <AboutPage />;
      case 'Team': return <TeamPage />;
      case 'Gallery': return <GalleryPage />;
      case 'Contact': return <ContactPage />;
      default: return <HomePage />;
    }
  };

  return (
    <div className="bg-gray-900">
      <Navigation currentPage={currentPage} setCurrentPage={setCurrentPage} />
      {renderPage()}
      <Footer />
    </div>
  );
}
