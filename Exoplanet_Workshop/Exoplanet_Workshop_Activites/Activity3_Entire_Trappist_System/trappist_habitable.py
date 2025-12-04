"""
TRAPPIST HABITABLE ZONE MISSION - BACKEND MODULE
Students use: mission = TRAPPISTHabitable() and everything just works!
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, Any
import pandas as pd
import os

class TRAPPISTHabitable:
    
    def __init__(self, data_file: str = "trappist_jwst_data.csv"):
        """
        ONE-LINE initialization: Loads data and sets up everything automatically!
        
        Parameters:
        -----------
        data_file : str, optional
            Path to your data file (default: "trappist_jwst_data.csv")
        """

        # REAL TRAPPIST-1 parameters
        self.all_planets: Dict[str, Dict[str, Any]] = {
            'b': {'period': 1.51, 'type': 'hot', 'temp_c': 127},
            'c': {'period': 2.42, 'type': 'hot', 'temp_c': 73},
            'd': {'period': 4.05, 'type': 'habitable', 'temp_c': 15, 'emoji': '🌍'},
            'e': {'period': 6.10, 'type': 'habitable', 'temp_c': -22, 'emoji': '❄️'},
            'f': {'period': 9.21, 'type': 'habitable', 'temp_c': -54, 'emoji': '🧊'},
            'g': {'period': 12.35, 'type': 'cold', 'temp_c': -98},
            'h': {'period': 18.77, 'type': 'cold', 'temp_c': -123}
        }
        
        self.habitable_planets = {k: v for k, v in self.all_planets.items() 
                                 if v['type'] == 'habitable'}
        
        # Try to load data automatically
        self.time, self.flux = self._load_data_safe(data_file)
        
        print("="*70)
        print("🌍 TRAPPIST-1 HABITABLE ZONE MISSION")
        print("="*70)
        print("\n✅ Mission initialized and ready!")
        
        if self.time is not None and len(self.time) > 0:
            print(f"📊 Data loaded: {len(self.time):,} points")
            print(f"📅 Time range: {self.time[0]:.1f} to {self.time[-1]:.1f} days")
        else:
            print("⚠️  Data not loaded - use mission.load_data() manually")
        
        print("\nUse these simple commands:")
        print("• mission.visualize_data()")
        print("• mission.find_habitable_periods()")
        print("• mission.run_habitability_dashboard()")
        print("="*70)
    
    # ============================================================
    # DATA LOADING (AUTOMATIC & SAFE)
    # ============================================================
    
    def _load_data_safe(self, filename: str) -> Tuple[np.ndarray, np.ndarray]:
        """Internal: Load data safely, return empty arrays if fails."""
        try:
            # Try multiple possible file locations
            possible_paths = [
                filename,
                f"Exoplanet_Workshop/Activity3_Entire_Trappist_System/{filename}",
                f"./{filename}",
                f"../{filename}"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    # Load with pandas (handles headers better)
                    df = pd.read_csv(path, comment='#')
                    
                    # Convert to numpy arrays
                    time = df.iloc[:, 0].values
                    flux = df.iloc[:, 1].values
                    
                    print(f"✅ Data loaded from: {path}")
                    return time, flux
            
            # If we get here, file not found
            print(f"❌ File not found: {filename}")
            print("   Tried:", possible_paths)
            return np.array([]), np.array([])
            
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")
            return np.array([]), np.array([])
    
    def load_data(self, filename: str = "trappist_jwst_data.csv") -> bool:
        """
        Manual data loader if auto-load fails.
        
        Parameters:
        -----------
        filename : str
            Path to your data file
        """
        self.time, self.flux = self._load_data_safe(filename)
        
        if len(self.time) > 0:
            return True
        return False
    
    # ============================================================
    # MAIN STUDENT COMMANDS (ONE-LINERS)
    # ============================================================
    
    def visualize_data(self) -> None:
        """
        ONE-LINE: Visualize the full TRAPPIST-1 system data.
        """
        if not self._has_data():
            return
        
        plt.figure(figsize=(14, 5))
        plt.plot(self.time, self.flux, 'k.', markersize=1, alpha=0.3)
        plt.title("FULL TRAPPIST-1 System Light Curve", fontsize=14)
        plt.xlabel("Time (days)")
        plt.ylabel("Normalized Brightness")
        plt.grid(alpha=0.3)
        
        # Add info box
        textstr = f'Data points: {len(self.time):,}\nTime span: {self.time[-1]:.0f} days'
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top', bbox=props)
        
        plt.show()
        
        print("\n🔍 DATA INTERPRETATION GUIDE:")
        print("• Each dot = one brightness measurement")
        print("• Dips = planets transiting (blocking starlight)")
        print("• Multiple overlapping dips = 7 planets!")
        print("• Your challenge: Find the habitable ones")
    
    def find_habitable_periods(self) -> None:
        """
        ONE-LINE: Find which orbital periods are in the habitable zone.
        """
        if not self._has_data():
            return
        
        print("\n" + "="*70)
        print("🔍 STEP 2: FIND HABITABLE ZONE PERIODS")
        print("="*70)
        
        # Show all periods found in data
        all_periods = [p['period'] for p in self.all_planets.values()]
        mystery_periods = [1.51, 2.42, 3.0, 4.05, 6.10, 9.21, 12.0]
        
        print("\n📋 ALL PERIODS IN THE DATA (The computer may be wrong so verify all of them, maybe using find_peiod):")
        print("-"*50)
        for i, period in enumerate(mystery_periods):
            source = "❌ Unknown" if period not in all_periods else ""
            for name, data in self.all_planets.items():
                if abs(data['period'] - period) < 0.01:
                    source = f"✅ Planet {name} ({data['type']})"
                    break
            
            print(f"{i+1:2}. {period:5.2f} days  {source}")
        
        print("\n💡 DISCUSSION QUESTION (2 minutes with partner):")
        print("Which 3 periods are in the 'Goldilocks Zone' (not too hot, not too cold)?")
        print("Hint: Look for 'habitable' type planets.")
        
        # Interactive reveal
        print("\n" + "-"*50)
        print("🎯 HABITABLE ZONE PLANETS (from NASA):")
        print("-"*50)
        for name, data in self.habitable_planets.items():
            print(f"  TRAPPIST-1{name}: {data['period']:.2f} days")
            print(f"     Temperature: {data['temp_c']}°C  {data.get('emoji', '')}")
        
        print("\n✅ KEY INSIGHT:")
        print("Habitable zone = MEDIUM periods (4-10 days)")
        print("Too hot = SHORT periods (<3 days)")
        print("Too cold = LONG periods (>10 days)")
        
        # Show period distribution
        self._plot_period_distribution()
    
    def run_habitability_dashboard(self) -> None:
        """
        ONE-LINE: Run full habitability analysis with visual dashboard.
        """
        if not self._has_data():
            return
        
        print("\n" + "="*70)
        print("🌡️ STEP 3: HABITABILITY DASHBOARD")
        print("="*70)
        
        # Create the dashboard
        self._create_habitability_dashboard()
        
        print("\n📊 HABITABILITY ASSESSMENT:")
        print("-"*50)
        
        for name, data in self.habitable_planets.items():
            temp = data['temp_c']
            period = data['period']
            emoji = data.get('emoji', '')
            
            # Calculate score
            score = self._calculate_habitability_score(temp)
            
            print(f"\n{emoji} TRAPPIST-1{name.upper()}:")
            print(f"  Period: {period:.2f} days")
            print(f"  Temperature: {temp}°C")
            print(f"  Score: {score:.2f}/1.0")
            
            # Custom analysis
            if name == 'd':
                print(f"  • Earth-like! Similar to our planet's temperature")
                print(f"  • Surface liquid water VERY likely")
            elif name == 'e':
                print(f"  • JWST's primary target for atmosphere study")
                print(f"  • With CO₂ atmosphere: could be 0-30°C")
            elif name == 'f':
                print(f"  • Possible subsurface ocean (like Europa)")
                print(f"  • Ice shell could protect life from radiation")
        
        print("\n" + "="*70)
    
    def real_science_connection(self) -> None:
        """
        ONE-LINE: Connect your analysis to real NASA/JWST science.
        """
        print("\n" + "="*70)
        print("🔭 STEP 4: REAL-WORLD SCIENCE CONNECTION")
        print("="*70)
        
        print("\n🎯 YOUR ANALYSIS MATTERS BECAUSE:")
        print("1. JWST is observing TRAPPIST-1 RIGHT NOW")
        print("2. Searching for water vapor, oxygen, methane in atmospheres")
        print("3. Could find BIOSIGNATURES (signs of life) in next 5 years!")
        
        print("\n📡 CURRENT JWST OBSERVATIONS:")
        print("• TRAPPIST-1e: Primary target (your 'most interesting' planet)")
        print("• Method: Transmission spectroscopy during transits")
        print("• Goal: Detect atmospheric gases that could indicate life")
        
        print("\n🌌 WHY THIS IS HISTORIC:")
        print("• First time we can study Earth-sized exoplanet atmospheres")
        print("• Could answer: 'Are we alone in the universe?'")
        print("• Your analysis today used REAL methods scientists use")
        
        print("\n" + "="*70)
        print("🏆 MISSION IMPACT:")
        print("="*70)
        print("\nYou didn't just complete an exercise.")
        print("You practiced the EXACT methods that might discover")
        print("the first evidence of life beyond Earth.")
        print("\nKeep looking up! 🔭✨")
    
    def save_report(self, team_name: str = "Team_Alpha") -> None:
        """
        ONE-LINE: Save your team's conclusions as a professional report.
        
        Parameters:
        -----------
        team_name : str
            Your team's name (e.g., "Team_Alpha")
        """
        if not self._has_data():
            return
        
        # Generate report
        report = self._generate_report(team_name)
        
        # Save to file
        filename = f"trappist_report_{team_name}.txt"
        with open(filename, "w") as f:
            f.write(report)
        
        print(f"\n✅ REPORT SAVED: {filename}")
        print("   Share with your instructor or keep as a science portfolio piece!")
        
        # Show preview
        print("\n📄 REPORT PREVIEW:")
        print("-"*50)
        lines = report.split('\n')[:15]  # First 15 lines
        for line in lines:
            print(line)
        print("... (full report in file)")
    
    # ============================================================
    # OPTIONAL EXPLORATION TOOLS
    # ============================================================
    
    def fold_at_period(self, period: float) -> None:
        """
        OPTIONAL: Fold data at a specific period to see transits.
        
        Parameters:
        -----------
        period : float
            Orbital period to test (in days)
        """
        if not self._has_data():
            return
        
        phase = (self.time % period) / period
        
        plt.figure(figsize=(12, 5))
        plt.scatter(phase, self.flux, s=1, alpha=0.1, color='blue')
        plt.title(f"Data Folded at {period:.2f} days")
        plt.xlabel("Phase (0 to 1 = one orbit)")
        plt.ylabel("Normalized Brightness")
        plt.ylim(0.995, 1.003)
        plt.grid(alpha=0.3)
        
        # Check if this matches known planet
        match = None
        for name, data in self.all_planets.items():
            if abs(data['period'] - period) < 0.05:
                match = (name, data)
                break
        
        if match:
            name, data = match
            plt.axvspan(0.48, 0.52, alpha=0.3, color='red', 
                       label=f'TRAPPIST-1{name} transit region')
            plt.legend()
            print(f"✅ Matches TRAPPIST-1{name} ({data['type']} planet)")
        else:
            plt.axvline(0.5, color='gray', linestyle='--', alpha=0.5,
                       label='Expected transit location')
            plt.legend()
            print(f"❌ No known planet at {period:.2f} days")
        
        plt.show()
    
    def show_full_system(self) -> None:
        """OPTIONAL: Visualize all 7 TRAPPIST-1 planets in context."""
        print("\n" + "="*70)
        print("🌌 FULL TRAPPIST-1 SYSTEM (7 Planets!)")
        print("="*70)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot 1: Orbital distances
        planets = list(self.all_planets.keys())
        periods = [self.all_planets[p]['period'] for p in planets]
        types = [self.all_planets[p]['type'] for p in planets]
        
        colors = {'hot': 'red', 'habitable': 'green', 'cold': 'blue'}
        color_list = [colors[t] for t in types]
        
        bars = ax1.bar(planets, periods, color=color_list, alpha=0.7)
        ax1.set_ylabel('Orbital Period (days)')
        ax1.set_title('All TRAPPIST-1 Planets')
        ax1.grid(alpha=0.3, axis='y')
        
        # Add habitable zone background
        ax1.axhspan(4, 10, alpha=0.2, color='lightgreen', 
                   label='Habitable Zone')
        
        # Label planets
        for bar, period, name in zip(bars, periods, planets):
            ax1.text(bar.get_x() + bar.get_width()/2, period + 0.5,
                    f"1{name}", ha='center', fontsize=9)
        
        ax1.legend()
        
        # Plot 2: Temperature comparison
        temps = [self.all_planets[p]['temp_c'] for p in planets]
        bars2 = ax2.bar(planets, temps, color=color_list, alpha=0.7)
        ax2.axhline(0, color='black', linestyle='-', alpha=0.3)
        ax2.axhspan(-20, 50, alpha=0.2, color='lightgreen',
                   label='Liquid water possible')
        ax2.set_ylabel('Temperature (°C)')
        ax2.set_title('Surface Temperatures')
        ax2.grid(alpha=0.3, axis='y')
        
        for bar, temp in zip(bars2, temps):
            ax2.text(bar.get_x() + bar.get_width()/2,
                    temp + (5 if temp > 0 else -10),
                    f'{temp}°C', ha='center', fontsize=9)
        
        ax2.legend()
        
        plt.suptitle('The TRAPPIST-1 System: 7 Earth-sized Worlds', fontsize=14)
        plt.tight_layout()
        plt.show()
        
        print("\n🔬 SYSTEM STATS:")
        print(f"• Total planets: 7")
        print(f"• Habitable zone planets: 3 (d, e, f)")
        print(f"• Closest orbit: 1.51 days (b)")
        print(f"• Farthest orbit: 18.77 days (h)")
        print(f"• Temperature range: 127°C to -123°C")
        
        print("\n🎯 WHY IT'S SPECIAL:")
        print("• Most Earth-sized planets around one star")
        print("• 3 in habitable zone")
        print("• Close enough for detailed study")
        print("• Best candidate for finding life beyond Earth")
    
    def solar_system_comparison(self) -> None:
        """Polar orbit comparison with space background + REAL Solar System distances + separate scales."""
        print("\n" + "="*70)
        print("🌞 COMPARISON: TRAPPIST-1 vs OUR SOLAR SYSTEM")
        print("="*70)

        # REAL Solar System orbital distances (in MILLIONS of km)
        solar_system_orbit_km = {
            'Mercury': 57.9,
            'Venus': 108.2,
            'Earth': 149.6,
            'Mars': 227.9
        }

        # Temperature info stays the same
        solar_system = {
            'Mercury': {'temp_c': 167, 'type': 'hot'},
            'Venus': {'temp_c': 464, 'type': 'hot'},
            'Earth': {'temp_c': 15,  'type': 'habitable'},
            'Mars': {'temp_c': -63, 'type': 'cold'}
        }

        fig, axes = plt.subplots(
            1, 2, figsize=(14, 6),
            subplot_kw={'projection': 'polar'}
        )
        fig.patch.set_facecolor("black")

        # Starry background
        for ax in axes:
            ax.set_facecolor("black")
            for _ in range(150):
                ax.scatter(
                    np.random.uniform(0, 2*np.pi),
                    np.random.uniform(0, 300),
                    s=np.random.uniform(5, 25),
                    color="white",
                    alpha=np.random.uniform(0.2, 0.8)
                )

        # ------------------------------------------------------------
        # TRAPPIST-1 SYSTEM (scale max 25)
        # ------------------------------------------------------------
        trappist_names = list(self.all_planets.keys())
        trappist_radii = np.array([self.all_planets[p]['period'] for p in trappist_names])
        angles = np.linspace(0, 2*np.pi, len(trappist_names), endpoint=False)

        ax = axes[0]
        ax.set_title("TRAPPIST-1 System", fontsize=12, color="white")

        # Star
        ax.scatter([0], [0], color="red", s=600, edgecolor="white", linewidth=1.2)

        # Planets
        ax.scatter(angles, trappist_radii, s=200, alpha=0.9, color="cyan")
        for ang, r, name in zip(angles, trappist_radii, trappist_names):
            ax.text(ang, r + 0.6, f"1{name}", fontsize=9, color="white", ha='center')

        # *** NEW: scale for TRAPPIST-1 ***
        ax.set_ylim(0, 25)

        ax.set_rticks([5, 10, 15, 20])
        ax.set_rlabel_position(-22)
        ax.tick_params(colors="white")
        ax.grid(alpha=0.25, color="gray")

        # ------------------------------------------------------------
        # SOLAR SYSTEM (scale max 300 million km)
        # ------------------------------------------------------------
        solar_names = list(solar_system.keys())
        solar_radii_km = np.array([solar_system_orbit_km[p] for p in solar_names])
        angles2 = np.linspace(0, 2*np.pi, len(solar_names), endpoint=False)

        ax2 = axes[1]
        ax2.set_title("Inner Solar System (Real Distances)", fontsize=12, color="white")

        # Sun
        ax2.scatter([0], [0], color="yellow", s=900, edgecolor="orange", linewidth=1.5)

        # Planets
        ax2.scatter(angles2, solar_radii_km, s=200, alpha=0.9, color="skyblue")
        for ang, r, name in zip(angles2, solar_radii_km, solar_names):
            ax2.text(ang, r + 8, name, fontsize=9, color="white", ha='center')

        # *** NEW: scale for Solar System ***
        ax2.set_ylim(0, 300)

        ax2.set_rticks([50, 100, 200])
        ax2.set_rlabel_position(-22)
        ax2.tick_params(colors="white")
        ax2.grid(alpha=0.25, color="gray")

        plt.suptitle("Real Distance Orbit Comparison • Space Theme", fontsize=14, color="white")
        plt.tight_layout()
        plt.show()

        print("\n📏 SCALE COMPARISON:")
        print(f"• TRAPPIST-1b orbit: 1.51 days")
        print(f"• Mercury orbit: 88 days")
        print(f"→ TRAPPIST-1 planets are 58x closer to their star!")
        
        print("\n🌡️ TEMPERATURE CONTEXT:")
        print(f"• TRAPPIST-1d: 15°C (Same as Earth!)")
        print(f"• Venus: 464°C (Runaway greenhouse)")
        print(f"• Mars: -63°C (Too cold without thick atmosphere)")
        
        print("\n💡 KEY INSIGHT:")
        print("Red dwarf stars (like TRAPPIST-1) are smaller and cooler,")
        print("so planets can orbit very close and still be habitable!")


    # ============================================================
    # INTERNAL HELPER METHODS
    # ============================================================
    
    def _has_data(self) -> bool:
        """Check if we have valid data."""
        if self.time is None or self.flux is None:
            print("❌ No data loaded! Run mission.load_data() first.")
            return False
        if len(self.time) == 0 or len(self.flux) == 0:
            print("❌ Data is empty! Check your file path.")
            return False
        return True
    
    def _plot_period_distribution(self) -> None:
        """Show period distribution with habitable zone highlighted."""
        periods = [p['period'] for p in self.all_planets.values()]
        types = [p['type'] for p in self.all_planets.values()]
        
        colors = {'hot': 'red', 'habitable': 'green', 'cold': 'blue'}
        color_list = [colors[t] for t in types]
        
        plt.figure(figsize=(10, 5))
        
        # Plot each planet
        for i, (period, color, name) in enumerate(zip(periods, color_list, self.all_planets.keys())):
            plt.scatter(period, 1, color=color, s=200, alpha=0.7, 
                       label=f'1{name}' if i < 3 else "")
            plt.text(period, 1.05, f'1{name}', ha='center', fontsize=9)
        
        # Highlight habitable zone
        plt.axvspan(4, 10, alpha=0.2, color='lightgreen', 
                   label='Habitable Zone')
        
        plt.xlabel("Orbital Period (days)")
        plt.title("TRAPPIST-1 Planet Distribution", fontsize=12)
        plt.yticks([])
        plt.xlim(0, 20)
        plt.grid(alpha=0.3, axis='x')
        
        # Custom legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='red', alpha=0.7, label='Hot (b, c)'),
            Patch(facecolor='green', alpha=0.7, label='Habitable (d, e, f)'),
            Patch(facecolor='blue', alpha=0.7, label='Cold (g, h)'),
            Patch(facecolor='lightgreen', alpha=0.2, label='Habitable Zone')
        ]
        
        plt.legend(handles=legend_elements, loc='upper right')
        plt.show()
    
    def _create_habitability_dashboard(self) -> None:
        """Create the main habitability dashboard visualization."""
        planets = list(self.habitable_planets.keys())
        periods = [self.habitable_planets[p]['period'] for p in planets]
        temps = [self.habitable_planets[p]['temp_c'] for p in planets]
        emojis = [self.habitable_planets[p].get('emoji', '') for p in planets]
        
        # Calculate scores
        scores = [self._calculate_habitability_score(t) for t in temps]
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        # Plot 1: Orbital Periods
        colors1 = ['lightgreen', 'lightblue', 'blue']
        bars1 = axes[0].bar(planets, periods, color=colors1, alpha=0.8, edgecolor='black')
        axes[0].set_ylabel('Orbital Period (days)')
        axes[0].set_title('Distance from Star')
        axes[0].grid(alpha=0.3, axis='y')
        
        for bar, period, emoji in zip(bars1, periods, emojis):
            axes[0].text(bar.get_x() + bar.get_width()/2, period + 0.3,
                        f'{emoji}\n{period} days', ha='center', fontsize=10)
        
        # Plot 2: Temperatures
        colors2 = ['green', 'lightblue', 'blue']
        bars2 = axes[1].bar(planets, temps, color=colors2, alpha=0.8, edgecolor='black')
        axes[1].axhline(0, color='black', linestyle='-', alpha=0.3)
        axes[1].axhspan(-20, 50, alpha=0.2, color='lightgreen', 
                       label='Liquid water possible')
        axes[1].set_ylabel('Temperature (°C)')
        axes[1].set_title('Surface Conditions')
        axes[1].grid(alpha=0.3, axis='y')
        axes[1].legend(loc='lower right')
        
        for bar, temp in zip(bars2, temps):
            axes[1].text(bar.get_x() + bar.get_width()/2,
                        temp + (3 if temp > 0 else -8),
                        f'{temp}°C', ha='center', fontsize=10, fontweight='bold')
        
        # Plot 3: Habitability Scores
        hab_colors = ['darkgreen', 'green', 'lightgreen']
        bars3 = axes[2].bar(planets, scores, color=hab_colors, alpha=0.8, edgecolor='black')
        axes[2].set_ylim(0, 1.1)
        axes[2].set_ylabel('Habitability Score')
        axes[2].set_title('Life Potential')
        axes[2].grid(alpha=0.3, axis='y')
        
        # Add score guides
        for y, color, label in [(0.8, 'darkgreen', 'Excellent'),
                               (0.6, 'green', 'Good'),
                               (0.4, 'yellow', 'Possible'),
                               (0.2, 'orange', 'Marginal')]:
            axes[2].axhline(y, color=color, linestyle='--', alpha=0.5, linewidth=0.8)
        
        for bar, score in zip(bars3, scores):
            label = "Excellent" if score > 0.8 else "Good" if score > 0.6 else "Possible"
            axes[2].text(bar.get_x() + bar.get_width()/2, score + 0.02,
                        f'{score:.2f}\n{label}', ha='center', fontsize=9)
        
        plt.suptitle('TRAPPIST-1 Habitable Zone Analysis', fontsize=16, y=1.05)
        plt.tight_layout()
        plt.show()
    
    def _calculate_habitability_score(self, temp: float) -> float:
        """Calculate habitability score based on temperature."""
        if -20 <= temp <= 50:  # Liquid water possible range
            score = 1.0 - abs(temp - 15) / 65  # Earth temp = 15°C is ideal
        elif -50 <= temp < -20:  # With greenhouse or subsurface
            score = 0.6 - (abs(temp) - 20) / 150
        else:
            score = 0.3
        
        return max(0.3, min(1.0, score))
    
    def _generate_report(self, team_name: str) -> str:
        """Generate a professional science report."""
        has_data = self._has_data()
        data_points = len(self.time) if has_data else 0
        time_range = f"{self.time[0]:.1f} to {self.time[-1]:.1f}" if has_data and len(self.time) > 1 else "N/A"
        
        report = f"""
{'='*70}
TRAPPIST-1 HABITABILITY ANALYSIS REPORT
{'='*70}

TEAM: {team_name}
DATE: {np.datetime64('today', 'D')}
MISSION: Habitable Zone Analysis

{'='*70}
EXECUTIVE SUMMARY
{'='*70}

Based on analysis of TRAPPIST-1 system light curve data, our team
has identified and assessed the three planets within the star's
habitable zone. TRAPPIST-1d shows the highest potential for
Earth-like conditions and possible surface liquid water.

{'='*70}
DATA ANALYSIS
{'='*70}

Data File: trappist_jwst_data.csv
Data Points: {data_points:,}
Time Range: {time_range} days
Analysis Method: Transit photometry + period folding

Identified Habitable Zone Periods:
  1. 4.05 days (TRAPPIST-1d)
  2. 6.10 days (TRAPPIST-1e)  
  3. 9.21 days (TRAPPIST-1f)

Excluded Periods (non-habitable):
  • 1.51, 2.42 days: Too hot (inner planets b, c)
  • 12.35, 18.77 days: Too cold (outer planets g, h)

{'='*70}
HABITABILITY ASSESSMENT
{'='*70}

1. TRAPPIST-1d 🌍
   • Orbital Period: 4.05 days
   • Temperature: 15°C (Earth-like!)
   • Habitability Score: {self._calculate_habitability_score(15):.2f}/1.0
   • Assessment: EXCELLENT - Similar temperature to Earth
   • Key Factor: Surface liquid water VERY likely

2. TRAPPIST-1e ❄️
   • Orbital Period: 6.10 days
   • Temperature: -22°C
   • Habitability Score: {self._calculate_habitability_score(-22):.2f}/1.0
   • Assessment: GOOD - Could be warmed by atmosphere
   • Key Factor: JWST primary target for atmospheric study

3. TRAPPIST-1f 🧊
   • Orbital Period: 9.21 days
   • Temperature: -54°C
   • Habitability Score: {self._calculate_habitability_score(-54):.2f}/1.0
   • Assessment: POSSIBLE - Subsurface ocean potential
   • Key Factor: Ice shell could protect from radiation

{'='*70}
RECOMMENDATIONS
{'='*70}

PRIORITY 1: Atmospheric Study (TRAPPIST-1e)
  • Use JWST transmission spectroscopy
  • Search for CO₂, H₂O, CH₄, O₂ signatures
  • Assess greenhouse warming potential

PRIORITY 2: Surface Characterization (TRAPPIST-1d)
  • Future direct imaging missions
  • Search for ocean glint, vegetation red edge
  • Climate modeling for water cycle

PRIORITY 3: Subsurface Exploration (TRAPPIST-1f)
  • Ice-penetrating radar studies
  • Search for Europa-like subsurface oceans
  • Assess radiation protection capabilities

{'='*70}
SCIENTIFIC IMPACT
{'='*70}

This analysis contributes to:
  1. Target selection for JWST observations
  2. Understanding red dwarf habitable zones
  3. Multi-planet system dynamics
  4. Biosignature detection strategies

The TRAPPIST-1 system represents our best opportunity to
discover life beyond Earth within the next decade.

{'='*70}
TEAM CONCLUSION
{'='*70}

We recommend focusing observational resources on TRAPPIST-1e,
as its position in the habitable zone combined with potential
atmospheric warming makes it the most promising candidate for
detecting biosignatures with current technology.

All three habitable zone planets warrant further study and
represent humanity's best chance to answer the fundamental
question: "Are we alone in the universe?"

{'='*70}
APPROVED BY: {team_name}
{'='*70}
"""
        return report


# ============================================================
# QUICK TEST
# ============================================================

if __name__ == "__main__":
    print("🧪 Testing TRAPPISTHabitable module...")
    
    # Test with auto-load
    mission = TRAPPISTHabitable("trappist_jwst_data.csv")
    
    # Try the main commands
    if mission._has_data():
        mission.visualize_data()
        mission.find_habitable_periods()
        mission.run_habitability_dashboard()
        mission.save_report("Test_Team")
    
    print("\n✅ Module ready for student use!")
    print("Students just need: mission = TRAPPISTHabitable()")