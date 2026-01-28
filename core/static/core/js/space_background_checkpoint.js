import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';

const initSpaceBackground = () => {
    const container = document.getElementById('canvas-container');
    if (!container) return;

    // --- Scene Setup ---
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0f1722, 0.015);

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // --- Interaction ---
    let mouseX = 0, mouseY = 0;
    const windowHalfX = window.innerWidth / 2;
    const windowHalfY = window.innerHeight / 2;

    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX - windowHalfX);
        mouseY = (event.clientY - windowHalfY);
    });

    // --- 1. Procedural Star Texture ---
    const getStarTexture = () => {
        const size = 64;
        const canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d');
        const center = size / 2;

        const gradient = ctx.createRadialGradient(center, center, 0, center, center, center);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
        gradient.addColorStop(0.2, 'rgba(220, 230, 255, 0.8)');
        gradient.addColorStop(0.5, 'rgba(100, 150, 255, 0.1)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, size, size);
        return new THREE.CanvasTexture(canvas);
    };

    // --- 2. Stars ---
    const starsGeometry = new THREE.BufferGeometry();
    const starsCount = 2000;
    const posArray = new Float32Array(starsCount * 3);
    const scaleArray = new Float32Array(starsCount);

    for (let i = 0; i < starsCount; i++) {
        posArray[i * 3] = (Math.random() - 0.5) * 40;
        posArray[i * 3 + 1] = (Math.random() - 0.5) * 40;
        posArray[i * 3 + 2] = (Math.random() - 0.5) * 40;
        scaleArray[i] = Math.random();
    }

    starsGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    starsGeometry.setAttribute('scale', new THREE.BufferAttribute(scaleArray, 1));

    const starsMaterial = new THREE.PointsMaterial({
        size: 0.12,
        map: getStarTexture(),
        transparent: true,
        opacity: 0.9,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        sizeAttenuation: true,
        color: 0xffffff
    });

    const starsMesh = new THREE.Points(starsGeometry, starsMaterial);
    scene.add(starsMesh);

    // --- 3. Airplanes & Trails ---
    const airplaneCount = 40;
    const airplanes = [];

    // Geometry
    const createPlaneGeometry = () => {
        const shape = new THREE.Shape();
        shape.moveTo(0, 0);
        shape.lineTo(-0.2, -0.1);
        shape.lineTo(0, 0.5);
        shape.lineTo(0.2, -0.1);
        shape.lineTo(0, 0);
        const geometry = new THREE.ShapeGeometry(shape);
        geometry.translate(0, -0.05, 0);
        return geometry;
    };

    const planeGeo = createPlaneGeometry();
    const planeMat = new THREE.MeshBasicMaterial({
        color: 0xffffff,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.9
    });

    // Trail Texture
    const getDotTexture = () => {
        const canvas = document.createElement('canvas');
        canvas.width = 16;
        canvas.height = 16;
        const ctx = canvas.getContext('2d');
        ctx.beginPath();
        ctx.arc(8, 8, 4, 0, 2 * Math.PI);
        ctx.fillStyle = '#ffffff';
        ctx.fill();
        return new THREE.CanvasTexture(canvas);
    };
    const dotTexture = getDotTexture();

    // Initialize 
    for (let i = 0; i < airplaneCount; i++) {
        const group = new THREE.Group();
        const plane = new THREE.Mesh(planeGeo, planeMat);

        // Slightly larger as requested (0.6 - 1.1)
        const scale = 0.6 + Math.random() * 0.5;
        plane.scale.set(scale, scale, scale);

        // Positioning
        const startRad = 10 + Math.random() * 10;
        const startAngle = Math.random() * Math.PI * 2;
        group.position.set(
            Math.cos(startAngle) * startRad,
            Math.sin(startAngle) * startRad,
            (Math.random() - 0.5) * 10
        );

        // Params
        const radius = 5 + Math.random() * 10;
        const speed = 0.2 + Math.random() * 0.3;
        const angleSpeed = (0.3 + Math.random() * 0.2) * (Math.random() > 0.5 ? 1 : -1);
        const driftZ = (Math.random() - 0.5) * 0.05;

        plane.rotateX(-Math.PI / 2);
        group.add(plane);

        // Trail Buffer
        const trailMaxPoints = 400;
        const trailPositions = new Float32Array(trailMaxPoints * 3);
        const trailAlphas = new Float32Array(trailMaxPoints);

        // Trail Material
        const trailMat = new THREE.ShaderMaterial({
            uniforms: {
                color: { value: new THREE.Color(0xaaddff) },
                tex: { value: dotTexture }
            },
            vertexShader: `
                attribute float alpha;
                varying float vAlpha;
                void main() {
                    vAlpha = alpha;
                    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
                    gl_PointSize = 4.0 * (30.0 / -mvPosition.z);
                    gl_Position = projectionMatrix * mvPosition;
                }
            `,
            fragmentShader: `
                uniform vec3 color;
                uniform sampler2D tex;
                varying float vAlpha;
                void main() {
                    gl_FragColor = vec4(color, vAlpha);
                    gl_FragColor = gl_FragColor * texture2D(tex, gl_PointCoord);
                }
            `,
            transparent: true,
            depthWrite: false,
            blending: THREE.AdditiveBlending
        });

        const trailGeo = new THREE.BufferGeometry();
        trailGeo.setAttribute('position', new THREE.BufferAttribute(trailPositions, 3));
        trailGeo.setAttribute('alpha', new THREE.BufferAttribute(trailAlphas, 1));

        const trailPoints = new THREE.Points(trailGeo, trailMat);
        scene.add(trailPoints);
        scene.add(group);

        airplanes.push({
            group: group,
            scale: scale, // Store scale relative to plane geometry
            trailPoints: trailPoints,
            trailPositions: trailPositions,
            trailAlphas: trailAlphas,
            trailIdx: 0,
            angle: startAngle,
            radius: radius,
            angleSpeed: angleSpeed * 0.01,
            driftZ: driftZ
        });
    }

    // Animation Loop
    const clock = new THREE.Clock();

    const animate = () => {
        const time = clock.getElapsedTime();

        // 1. Stars Interactive
        const targetRotX = mouseY * 0.0002;
        const targetRotY = mouseX * 0.0002;
        starsMesh.rotation.x += 0.05 * (targetRotX - starsMesh.rotation.x);
        starsMesh.rotation.y += 0.05 * (targetRotY - starsMesh.rotation.y);

        // 2. Airplanes
        airplanes.forEach(obj => {
            // Spiral
            obj.angle += obj.angleSpeed;
            obj.group.position.x = Math.cos(obj.angle) * obj.radius;
            obj.group.position.y = Math.sin(obj.angle) * obj.radius;
            obj.group.position.z += obj.driftZ;

            // Loop Z
            if (obj.group.position.z > 20) obj.group.position.z = -20;
            if (obj.group.position.z < -20) obj.group.position.z = 20;

            // Orientation
            const tangentX = -Math.sin(obj.angle);
            const tangentY = Math.cos(obj.angle);

            // Tangent Logic for lookAt:
            // Since we use lookAt(target), and objects face -Z towards target.
            // If tangent is forward, we lookAt(pos + tangent).
            // This means -Z is Forward. +Z is Backward.
            // Tail is at +Z.
            const target = obj.group.position.clone().add(new THREE.Vector3(tangentX, tangentY, 0));
            obj.group.lookAt(target);

            // --- Trail Emission ---
            if (renderer.info.render.frame % 3 === 0) {
                const idx = obj.trailIdx;
                const positions = obj.trailPositions;
                const alphas = obj.trailAlphas;

                // Calculate Tail Position
                // Tangent vector is normalized direction of travel.
                // We want to go backwards -> -tangent.
                // Distance = Plane geometry length (~0.6 total) * scale * ~0.5 (halfway) + slight gap
                // Geometry is translated so center is roughly mid-body. Tail is ~0.1 units "back" (visually).
                // Actually after rotation, +Z is back.
                // Offset scalar roughly 0.25 * scale ensures we are behind the wings.
                const offset = 0.4 * obj.scale;

                // Direction: -Tangent (Backwards in World Space)
                // Actually, simply: pos - (tangent * offset)
                const tailX = obj.group.position.x - (tangentX * offset);
                const tailY = obj.group.position.y - (tangentY * offset);
                // Tangent is xy only, need to account for z orientation? 
                // The plane is "flat" on the spiral cylinder, so local Z is parallel to spiral tangent?
                // Yes, group.lookAt aligns -Z to tangent. So +Z axis IS -tangent.
                // But the tangent vector (tangentX, tangentY, 0) is unit length approx.
                // Wait, if angleSpeed is small, movement is small... no tangent is derived from circle math, it's unit vector.
                // So simpler approach:
                // tailPos = groupPos + (BackwardVector * offset)
                // BackwardVector = Vector(-tangentX, -tangentY, 0).normalize()

                // Better yet: group.lookAt aligns the local -Z axis to the target.
                // So the local Z axis points backwards.
                // We can just transform local point (0,0,offset) to world.
                // BUT computing world matrix every frame inside loop is heavy? 
                // Actually Three.js updates matrices in render(), not update(). 
                // So obj.group.updateMatrixWorld() is needed if we use localToWorld here.
                // It's just 40 planes, it's cheap.

                obj.group.updateMatrixWorld(); // Ensure matrix is current

                // Create vector for tail offset (local space)
                // Plane is rotated -90 X. 
                // Geometry: Tail is at (0, 0) roughly in shape, translated to (0, -0.05, 0).
                // After RotateX(-90): 
                // Local Y -> World -Z (Forward)
                // Local -Y -> World +Z (Backward)
                // Tail is at "bottom" of Y shape (-0.1). So it becomes "back" (+Z).
                // So a positive Z offset in local space is correct.
                const vec = new THREE.Vector3(0, 0.25 * obj.scale, 0); // Local: +Y is nose? No wait. 
                // Let's stick to world math, less rotation confusion.
                // Use the calculated tangent.

                const normTangent = new THREE.Vector3(tangentX, tangentY, 0).normalize();

                positions[idx * 3] = obj.group.position.x - (normTangent.x * offset);
                positions[idx * 3 + 1] = obj.group.position.y - (normTangent.y * offset);
                positions[idx * 3 + 2] = obj.group.position.z; // Z drift is negligible for orientation usually

                alphas[idx] = 1.0;

                obj.trailIdx = (obj.trailIdx + 1) % obj.trailAlphas.length;

                obj.trailPoints.geometry.attributes.position.needsUpdate = true;
                obj.trailPoints.geometry.attributes.alpha.needsUpdate = true;
            }

            // Decay
            const alphas = obj.trailAlphas;
            for (let k = 0; k < alphas.length; k++) {
                if (alphas[k] > 0) alphas[k] -= 0.002;
                if (alphas[k] < 0) alphas[k] = 0;
            }
            obj.trailPoints.geometry.attributes.alpha.needsUpdate = true;
        });

        renderer.render(scene, camera);
        requestAnimationFrame(animate);
    };

    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
};

document.addEventListener('DOMContentLoaded', initSpaceBackground);
