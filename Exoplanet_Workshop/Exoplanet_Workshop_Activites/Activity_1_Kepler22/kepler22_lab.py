import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider
from IPython.display import clear_output
import warnings
warnings.filterwarnings('ignore')


class Kepler_Tool:

    """
    TRANSIT LAB - Interactive planet transit analysis for astronomy students
    
    Purpose:
    ----------
    This lab simulates the analysis of exoplanet transit data. Students can:

    1. Load telescope data of star brightness over time
    2. Visually identify transit dips caused by a planet passing in front of its star
    3. Interactively fit a transit model using physical parameters
    4. Analyze residuals to assess fit quality
    5. Get hints for orbital period
    
    Scientific Background:
    ----------
    The transit method detects exoplanets by measuring the slight dimming of a star
    when a planet passes in front of it. The depth of the dip indicates the planet's size
    relative to the star, while the timing between dips reveals the orbital period.
    
    Parameters:
    ----------
    seed : int, optional
        Random seed for reproducible data generation (default: 42)
    """
    

    def __init__(self, seed=42):
        """Initialize the transit lab with a random seed for reproducibility."""

        np.random.seed(seed)
        print("🚀 Transit Lab initialized. Ready to detect Kepler-22B!")
    
    # ============================================================================
    # CORE PHYSICS: Transit Light Curve Model
    # ============================================================================
    
    def _transit_model(self, time, planet_size, orbital_period, impact_parameter):
        """
        Generate a simulated transit light curve based on physical parameters.
        
        Parameters:
        ----------
        time : array
            Time array in days
        planet_size : float
            Planet radius relative to star radius (Rp/Rs)
        orbital_period : float
            Orbital period in days
        impact_parameter : float
            Distance from center of star (0-1), affects transit duration
        
        Returns:
        ----------
        flux : array
            Normalized flux (brightness) over time
        """
        # Phase-fold the time series
        phase = (time % orbital_period) / orbital_period
        center = 0.5  # Transit center at phase 0.5
        
        # Calculate transit properties
        transit_depth = planet_size**2  # Depth proportional to area ratio
        transit_duration = 0.1 * (impact_parameter / 10)  # Duration increases with distance
        
        # Initialize flux array
        flux = np.ones_like(time)
        
        # Identify transit points
        distance_from_center = np.abs(phase - center)
        in_transit = distance_from_center < transit_duration
        
        # Apply transit depth
        if np.any(in_transit):
            # Simple trapezoid model (flat bottom, sloping edges)
            mid_transit = distance_from_center < (transit_duration * 0.6)
            flux[mid_transit] = 1 - transit_depth
            
            # Transit edges (quadratic ingress/egress)
            edges = in_transit & ~mid_transit
            if np.any(edges):
                # Normalized distance from center (0 at edge, 1 at end of ingress/egress)
                edge_distance = (distance_from_center[edges] - transit_duration * 0.6) / (transit_duration * 0.4)
                flux[edges] = 1 - transit_depth * (1 - edge_distance**2)
        
        return flux
    
    # ============================================================================
    # STUDENT FUNCTIONS: Data Loading and Visualization
    # ============================================================================
    
    def load_data(self, filename="kepler22b_data.csv"):
        """
        Load transit data from a CSV file.
        
        Parameters:
        ----------
        filename : str
            Path to the data file
        
        Returns:
        ----------
        time, flux : arrays
            Time and flux arrays from the data file
        """
        print(f"📂 Loading data from {filename}...")
        
        try:
            data = np.loadtxt(filename, delimiter=',', skiprows=5)
            time = data[:, 0]
            flux = data[:, 1]
            
            print(f"✅ Successfully loaded {len(time)} data points")
            print(f"📊 Time range: {time[0]:.1f} to {time[-1]:.1f} days")
            
            return time, flux
            
        except FileNotFoundError:
            print(f"❌ Error: File '{filename}' not found.")
            print("💡 Make sure the data file exists in the current folder.")
            return None, None
    
    def plot_light_curve(self, time, flux, title="Kepler Telescope Data"):
        """
        Plot the light curve (brightness vs time).
        
        Parameters:
        ----------
        time : array
            Time array in days
        flux : array
            Normalized flux measurements
        title : str, optional
            Plot title
        """
        plt.figure(figsize=(12, 5))
        
        plt.scatter(time, flux, s=1, alpha=0.7, color='navy', label='Observations')
        plt.xlabel("Time (days)", fontsize=12)
        plt.ylabel("Normalized Flux", fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(alpha=0.3, linestyle='--')
        plt.legend(loc='upper right')
        
        # Add annotation about transit dips
        plt.annotate('Transit dips →', xy=(0.02, 0.95), xycoords='axes fraction',
                    fontsize=11, color='darkred', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    # ============================================================================
    # STUDENT FUNCTIONS: Interactive Fitting
    # ============================================================================
    
    def interactive_fit(self, time, flux):
        """
        Interactive fitting with real-time analysis
        WITHOUT zoomed view and WITH fixed fonts
        """
        print("🎯 INTERACTIVE TRANSIT DETECTIVE")
        print("=" * 60)
        print("ADJUST SLIDERS to find the hidden planet!")
        print("Watch the ANALYSIS update in real-time.")
        print("=" * 60)
        
        @interact(
            planet_size=FloatSlider(
                min=0.005, max=0.09, step=0.005, value=0.05,
                description='Planet Size (Rp/Rs):',
                style={'description_width': 'initial'},
                continuous_update=True
            ),
            orbital_period=FloatSlider(
                min=220, max=350, step=0.5, value=260,
                description='Orbital Period (days):',
                style={'description_width': 'initial'},
                continuous_update=True
            ),
            orbital_speed=FloatSlider(
                min=0.5, max=8.0, step=0.1, value=4.0,
                description='Orbital Speed Factor:',
                style={'description_width': 'initial'},
                continuous_update=True
            )
        )
        def update_fit(planet_size, orbital_period, orbital_speed):
            clear_output(wait=True)
            
            # Generate model
            model_flux = self._transit_model(time, planet_size, orbital_period, orbital_speed)
            
            # Calculate fit quality
            residuals = flux - model_flux
            rms_error = np.sqrt(np.mean(residuals**2))
            base_score = 100 * np.exp(-rms_error * 1000)
            score = np.clip(base_score, 0, 100)
            
            # ============================================
            # REAL-TIME ANALYSIS CALCULATIONS
            # ============================================
            
            # 1. Transit depth (how deep is the dip?)
            transit_depth = planet_size**2 * 100  # Percentage
            
            # 2. Transit duration (how long does it last?)
            transit_duration = 0.1 * orbital_speed * np.sqrt(orbital_period/290)
            
            # 3. Planet classification (SIMPLE SYMBOLS - no font warnings)
            if planet_size < 0.04:
                size_class = "Earth-sized"
                planet_type = "Rocky World"
                likely_composition = "Rock/iron like Earth"
            elif planet_size < 0.085:
                size_class = "Super-Earth"
                planet_type = "Large Rocky"
                likely_composition = "Rock with thick atmosphere"
            elif planet_size < 0.1:
                size_class = "Neptune-sized"
                planet_type = "Ice Giant"
                likely_composition = "Hydrogen/helium with icy core"
            else:
                size_class = "Jupiter-sized"
                planet_type = "Gas Giant"
                likely_composition = "Mostly hydrogen/helium"
            
            # 4. Temperature estimation (SIMPLE TEXT - no emojis)
            if orbital_period < 200:
                temp_class = "VERY HOT"
                est_temp = "700-1000°C"
                habitable = "Not habitable"
            elif orbital_period < 250:
                temp_class = "WARM"
                est_temp = "100-300°C"
                habitable = "Too hot for life"
            elif orbital_period < 300:
                temp_class = "EARTH-LIKE"
                est_temp = "0-100°C"
                habitable = "Possibly habitable!"
            else:
                temp_class = "COLD"
                est_temp = "-100 to 0°C"
                habitable = "Maybe with greenhouse"
            
            # 5. Orbital characteristics
            orbital_distance = (orbital_period/365.25)**(2/3)  # AU approximation
            
            # ============================================
            # CREATE THE VISUALIZATION - NO ZOOMED VIEW
            # ============================================
            
            fig = plt.figure(figsize=(16, 10))
            
            # Left: Data vs Model (BIGGER - takes zoomed view space)
            ax1 = plt.subplot(2, 2, 1)
            ax1.scatter(time, flux, s=1, alpha=0.4, color='navy', label='Telescope Data')
            ax1.plot(time, model_flux, 'r-', linewidth=2.5, 
                    label=f'Your Model (Score: {score:.0f}/100)', alpha=0.8)
            ax1.set_ylabel('Normalized Flux', fontsize=12)
            ax1.set_title('DATA vs MODEL FIT', fontweight='bold')
            ax1.legend(loc='upper right', fontsize=10)
            ax1.grid(alpha=0.2, linestyle='--')
            ax1.set_ylim(0.994, 1.004)
            
            # Right: Residuals
            ax2 = plt.subplot(2, 2, 2)
            ax2.scatter(time, residuals, s=1, alpha=0.6, color='green')
            ax2.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.7)
            ax2.set_xlabel('Time (days)', fontsize=12)
            ax2.set_ylabel('Residuals', fontsize=12)
            ax2.set_title('RESIDUALS (Data - Model)', fontweight='bold')
            ax2.grid(alpha=0.2, linestyle='--')
            
            # Bottom: ANALYSIS RESULTS (2 panels now, side by side)
            
            # Panel 1: Planet Properties
            ax3 = plt.subplot(2, 2, 3)
            ax3.axis('off')
            analysis_text = f"""
            PLANET PROPERTIES
            
            SIZE:
              • Rp/Rs: {planet_size:.3f}
              • Type: {size_class}
              • {planet_type}
            
            ORBIT:
              • Period: {orbital_period:.1f} days
              • Distance: ~{orbital_distance:.2f} AU
              • Temperature class: {temp_class}
            
            TEMPERATURE:
              • Estimated: {est_temp}
              • Habitable: {habitable}
            """
            ax3.text(0.05, 0.95, analysis_text, transform=ax3.transAxes,
                    verticalalignment='top', fontsize=11,
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3),
                    family='monospace')
            
            # Panel 2: Transit Analysis & Feedback
            ax4 = plt.subplot(2, 2, 4)
            ax4.axis('off')
            
            # Score-based feedback (SIMPLE TEXT)
            if score > 50:
                feedback = "EXCELLENT FIT! Matches Kepler-22b data well!"
                context = "You've found an Earth-sized world in the habitable zone!"
            elif score > 40:
                feedback = "GOOD FIT! Close to the real parameters."
                context = "This could be a super-Earth or mini-Neptune."
            elif score > 35:
                feedback = "DECENT FIT. Keep adjusting!"
                context = "Look for a deeper dip with the right spacing."
            else:
                feedback = "KEEP TRYING! Adjust sliders carefully."
                context = "Check period spacing and transit depth."
            
            transit_text = f"""
            TRANSIT ANALYSIS
            
            DIP CHARACTERISTICS:
              • Depth: {transit_depth:.3f}%
              • Duration: {transit_duration:.3f} days
              • Frequency: Every {orbital_period:.1f} days
            
            FIT QUALITY:
              • Score: {score:.0f}/100
            
            FEEDBACK:
              {feedback}
            
            SCIENCE CONTEXT:
              {context}
            
            NEXT STEPS:
              • Maximize your score (>50 is great!)
              • Match the transit shape
              • Note the best parameters
            """
            ax4.text(0.05, 0.95, transit_text, transform=ax4.transAxes,
                    verticalalignment='top', fontsize=11,
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3),
                    family='monospace')
            
            plt.suptitle('REAL-TIME EXOPLANET ANALYSIS', fontsize=14, fontweight='bold', y=1.02)
            plt.tight_layout()
            plt.show()
            
            # ============================================
            # CONSOLE OUTPUT
            # ============================================
            
            print("="*60)
            print("REAL-TIME ANALYSIS UPDATE")
            print("="*60)
            
            print(f"\nCURRENT PARAMETERS:")
            print(f"  • Planet Size (Rp/Rs): {planet_size:.3f}")
            print(f"  • Orbital Period: {orbital_period:.1f} days")
            print(f"  • Speed Factor: {orbital_speed:.1f}")
            
            print(f"\nFIT SCORE: {score:.0f}/80")
            
            # Simple progress bar
            bar_length = 20
            filled = int(bar_length * score / 100)
            bar = '#' * filled + '-' * (bar_length - filled)
            print(f"  [{bar}] {score:.0f}%")
            
            print(f"\nFEEDBACK: {feedback}")
            
            # Hints if score is low
            if score < 50:
                print(f"\nHINTS:")
                if rms_error > 0.001:
                    print("  • Try adjusting the PERIOD slider")
                    print("  • Look for repeating pattern every ~290 days")
                if planet_size < 0.04:
                    print("  • The transit dip should be DEEPER")
                    print("  • Increase planet size")
                print("  • Try: Period = 290, Size > 0.05, Speed = 0.5 - 1.5")