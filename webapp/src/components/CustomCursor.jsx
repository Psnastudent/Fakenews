import { useEffect, useRef } from 'react';
import gsap from 'gsap';

export default function CustomCursor() {
  const cursorRef = useRef(null);
  const dotRef = useRef(null);

  useEffect(() => {
    const cursor = cursorRef.current;
    const dot = dotRef.current;
    
    // Set initial position
    gsap.set(cursor, { xPercent: -50, yPercent: -50 });
    gsap.set(dot, { xPercent: -50, yPercent: -50 });

    let mouseX = 0;
    let mouseY = 0;

    const onMouseMove = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      
      // Move dot instantly
      gsap.set(dot, { x: mouseX, y: mouseY });
      
      // Move circle with a lag
      gsap.to(cursor, {
        x: mouseX,
        y: mouseY,
        duration: 0.6,
        ease: 'power3.out'
      });
    };

    const onHover = () => {
      gsap.to(cursor, {
        scale: 1.5,
        backgroundColor: 'rgba(255, 107, 74, 0.2)',
        borderColor: 'transparent',
        duration: 0.3
      });
      gsap.to(dot, { scale: 0, duration: 0.3 });
    };

    const onLeave = () => {
      gsap.to(cursor, {
        scale: 1,
        backgroundColor: 'transparent',
        borderColor: 'rgba(255, 255, 255, 0.3)',
        duration: 0.3
      });
      gsap.to(dot, { scale: 1, duration: 0.3 });
    };

    window.addEventListener('mousemove', onMouseMove);

    // Add listeners to interactive elements
    const interactiveElements = document.querySelectorAll('a, button');
    interactiveElements.forEach((el) => {
      el.addEventListener('mouseenter', onHover);
      el.addEventListener('mouseleave', onLeave);
    });

    return () => {
      window.removeEventListener('mousemove', onMouseMove);
      interactiveElements.forEach((el) => {
        el.removeEventListener('mouseenter', onHover);
        el.removeEventListener('mouseleave', onLeave);
      });
    };
  }, []);

  return (
    <>
      <div 
        ref={cursorRef} 
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '40px',
          height: '40px',
          borderRadius: '50%',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          pointerEvents: 'none',
          zIndex: 9999,
          mixBlendMode: 'difference'
        }}
      />
      <div 
        ref={dotRef}
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '6px',
          height: '6px',
          backgroundColor: '#ff6b4a',
          borderRadius: '50%',
          pointerEvents: 'none',
          zIndex: 10000,
        }}
      />
    </>
  );
}
