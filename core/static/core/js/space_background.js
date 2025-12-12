import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';

const initSpaceBackground = () => {
    const container = document.getElementById('canvas-container');
    if (!container) return;

    // Scene Setup
    const scene = new THREE.Scene();

    // Camera
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    // Renderer
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Particles (Stars)
    const starsGeometry = new THREE.BufferGeometry();
    const starsCount = 2000;
    const posArray = new Float32Array(starsCount * 3);

    for (let i = 0; i < starsCount * 3; i++) {
        // Spread stars in a wide 3D space
        posArray[i] = (Math.random() - 0.5) * 15;
    }

    starsGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    // Star Material
    const starsMaterial = new THREE.PointsMaterial({
        size: 0.02, // Small, crisp stars
        color: 0xffffff,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending
    });

    // Star Mesh
    const starsMesh = new THREE.Points(starsGeometry, starsMaterial);
    scene.add(starsMesh);

    // Mouse Interaction
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const windowHalfX = window.innerWidth / 2;
    const windowHalfY = window.innerHeight / 2;

    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX - windowHalfX);
        mouseY = (event.clientY - windowHalfY);
    });

    // Animation Loop
    const clock = new THREE.Clock();

    const animate = () => {
        targetX = mouseX * 0.001;
        targetY = mouseY * 0.001;

        // Smooth rotation
        starsMesh.rotation.y += 0.0005; // Constant slow rotation
        starsMesh.rotation.x += 0.05 * (targetY - starsMesh.rotation.x);
        starsMesh.rotation.y += 0.05 * (targetX - starsMesh.rotation.y);

        // Gentle floating effect
        const time = clock.getElapsedTime();
        starsMesh.position.y = Math.sin(time * 0.5) * 0.2;

        renderer.render(scene, camera);
        requestAnimationFrame(animate);
    };

    animate();

    // Resize Handler
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
};

document.addEventListener('DOMContentLoaded', initSpaceBackground);
