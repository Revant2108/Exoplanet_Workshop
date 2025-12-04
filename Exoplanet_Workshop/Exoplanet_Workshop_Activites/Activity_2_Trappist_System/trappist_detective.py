"""
TRAPPIST-1 DETECTIVE MISSION
Activity 2: Find the two hidden planets in TRAPPIST-1 system

Students use in Jupyter like:
from trappist_detective import TRAPPISTMission
mission = TRAPPISTMission()
mission.load_data()  # Loads the pre-made data file

# Guided steps:
mission.step1_view_data()
mission.step2_fold_first_planet()
# etc.

# OR for exploration:
mission.fold_at_period(your choosen guess)  # Try different periods!
"""

import numpy as np
import matplotlib.pyplot as plt

class TRAPPISTMission:
    
    def __init__(self):
        """
        Initialize the TRAPPIST-1 detective mission.
        """
        # Real TRAPPIST-1 parameters (from NASA)
        self.planet_b_period = 1.51  # days
        self.planet_c_period = 2.42  # days
        
        # Data storage
        self.time = None
        self.flux = None
        
        print("="*60)
        print("🔭 TRAPPIST-1 DETECTIVE MISSION 🔭")
        print("="*60)
        print("\nMission: Find the hidden planets orbiting TRAPPIST-1")
        print("This red dwarf star has at least 7 Earth-sized planets!")
        print("Your task: Find the two innermost ones.")
        print("\n" + "="*60)
    
    def load_data(self, filename="trappist1_data.csv"):
        """
        Load TRAPPIST-1 data from a CSV file.
        
        Parameters:
        -----------
        filename : str
            Name of the file to load (pre-made data file)
        """
        try:
            # Load the data (skip header lines starting with #)
            data = np.loadtxt(filename, delimiter=',', comments='#')
            
            self.time = data[:, 0]
            self.flux = data[:, 1]
            
            print(f"✅ Data loaded from: {filename}")
            print(f"📊 {len(self.time):,} data points")
            print(f"📅 Time range: {self.time[0]:.1f} to {self.time[-1]:.1f} days")
            
            return self.time, self.flux
            
        except FileNotFoundError:
            print(f"❌ ERROR: File '{filename}' not found!")
            print("Make sure 'trappist1_data.csv' is in the same folder.")
            return None, None
    
    # ============================================================
    # 🔧 INTERACTIVE TOOL: FOLD AT ANY PERIOD
    # ============================================================
    
    def fold_at_period(self, period):
        """
        Interactive tool: Fold the data at ANY period to search for planets.
        
        Students can experiment with different periods to find transits.
        
        Parameters:
        -----------
        period : float
            The orbital period to test (in days)
        """
        if self.time is None or self.flux is None:
            print("❌ ERROR: No data loaded! Call mission.load_data() first")
            return
        
        print(f"\n🔍 Testing period: {period} days")
        print("-" * 40)
        
        # Fold the data at the given period
        phase = (self.time % period) / period
        
        plt.figure(figsize=(12, 5))
        plt.scatter(phase, self.flux, s=2, alpha=0.3, color='blue')
        plt.title(f"Data Folded at {period} days")
        plt.xlabel("Phase (0 to 1 = one complete orbit)")
        plt.ylabel("Normalized Brightness")
        plt.ylim(0.995, 1.003)
        plt.grid(alpha=0.3)
        
        # Check if this period is close to known planets
        if abs(period - 1.51) < 0.05:
            plt.axvspan(0.45, 0.55, alpha=0.2, color='red', 
                       label='TRAPPIST-1b transit!')
            print("🎯 BINGO! You found TRAPPIST-1b!")
            print(f"   Real period: 1.51 days")
        elif abs(period - 2.42) < 0.05:
            plt.axvspan(0.48, 0.52, alpha=0.2, color='green',
                       label='TRAPPIST-1c transit!')
            print("🎯 BINGO! You found TRAPPIST-1c!")
            print(f"   Real period: 2.42 days")
        else:
            # Mark the center where a transit would appear
            plt.axvline(0.5, color='gray', linestyle='--', alpha=0.5,
                       label='Expected transit location')
            print("❌ No clear transit detected.")
            print("   Try a different period!")
        
        plt.legend()
        plt.show()
        
        # Give hints if they're close
        if 1.4 < period < 1.6 and abs(period - 1.51) >= 0.05:
            print(f"💡 Hint: You're close! Try adjusting slightly...")
        elif 2.3 < period < 2.5 and abs(period - 2.42) >= 0.05:
            print(f"💡 Hint: Getting warm! Fine-tune your period...")
        
        return phase
    
    # ============================================================
    # 📝 GUIDED STEP-BY-STEP MISSION
    # ============================================================
    
    def step1_view_data(self):
        """
        STEP 1: View the raw telescope data.
        Students see the messy light curve and look for patterns.
        """
        if self.time is None or self.flux is None:
            print("❌ ERROR: No data loaded! Call mission.load_data() first")
            return
        
        print("\n" + "="*60)
        print("STEP 1: EXAMINE THE RAW DATA")
        print("="*60)
        
        plt.figure(figsize=(14, 5))
        plt.plot(self.time, self.flux, 'k.', markersize=2, alpha=0.5)
        plt.title("TRAPPIST-1: Raw Telescope Data (20 days)")
        plt.xlabel("Time (days)")
        plt.ylabel("Normalized Brightness")
        plt.ylim(0.995, 1.003)
        plt.grid(alpha=0.3)
        plt.show()
        
        print("\n🔍 YOUR TASK:")
        print("Look at the data. What do you notice?")
        print("• Can you see any repeating patterns?")
        print("• Why is it so messy?")
    
    def step2_fold_first_planet(self):
        """
        STEP 2: Fold the data to find the first planet.
        Students fold at 1.51 days and discover TRAPPIST-1b.
        """
        print("\n" + "="*60)
        print("STEP 2: FIND THE FIRST PLANET")
        print("="*60)
        print("Let's use the fold_at_period tool to search...")
        
        # Use the interactive tool with the correct period
        self.fold_at_period(1.51)
    
    def step3_remove_planet(self):
        """
        STEP 3: Remove the first planet's signal.
        Simple masking technique to 'subtract' planet b.
        """
        if self.time is None or self.flux is None:
            print("❌ ERROR: No data loaded!")
            return
        
        print("\n" + "="*60)
        print("STEP 3: REMOVE PLANET b")
        print("="*60)
        
        # Show planet b's transits
        phase = (self.time % 1.51) / 1.51
        transit_mask = (phase > 0.45) & (phase < 0.55)
        
        plt.figure(figsize=(12, 5))
        plt.scatter(self.time, self.flux, s=2, alpha=0.1, color='gray')
        plt.scatter(self.time[transit_mask], self.flux[transit_mask], 
                   s=10, alpha=0.7, color='red', label='Planet b transits')
        plt.title("Identifying Planet b's Transits")
        plt.xlabel("Time (days)")
        plt.ylabel("Brightness")
        plt.ylim(0.995, 1.003)
        plt.grid(alpha=0.3)
        plt.legend()
        plt.show()
        
        print(f"✅ Found {np.sum(transit_mask)} transit points for Planet b")
        print("\n🔧 Next step: Remove these points and search for more planets!")
    
    def step4_find_second_planet(self):
        """
        STEP 4: Find the second hidden planet.
        """
        print("\n" + "="*60)
        print("STEP 4: FIND THE SECOND PLANET")
        print("="*60)
        print("Now search in the 'cleaned' data...")
        
        # Students can use fold_at_period to discover planet c
        print("\n💡 Try using: mission.fold_at_period(2.42)")
        print("   Or experiment with other periods!")
        
        # Optional: Show a preview
        self.fold_at_period(2.42)
    
    def step5_conclusion(self):
        """
        STEP 5: Mission conclusion and real-world context.
        """
        print("\n" + "="*60)
        print("STEP 5: MISSION CONCLUSION")
        print("="*60)
        
        print("\n🏆 MISSION ACCOMPLISHED!")
        print("You discovered:")
        print(f"• TRAPPIST-1b: {self.planet_b_period} day orbit")
        print(f"• TRAPPIST-1c: {self.planet_c_period} day orbit")
        
        print("\n🌍 REAL-WORLD CONTEXT:")
        print("• TRAPPIST-1 has 7 Earth-sized planets!")
        print("• 3 are in the 'habitable zone' for liquid water")
        print("• This is one of the most promising systems for life!")
        
        print("\n🔬 TRY ANSWERING THESE:")
        print("1. mission.fold_at_period(3.0) - What happens?")
        print("2. mission.fold_at_period(4.0) - Any signal?")
        print("3. What if there was a third planet?")
    
