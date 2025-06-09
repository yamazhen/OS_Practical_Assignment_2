import os
import time
from collections import defaultdict

import matplotlib.pyplot as plt


class Simulator:
    def __init__(self):
        pass
    
    def clear_screen(self):
        os.system('clear')
    
    def visual_demonstration(self, reference_string, frame_size, algorithm_name):
        print(f"\n{'='*60}")
        print(f"VISUAL DEMONSTRATION: {algorithm_name.upper()} ALGORITHM")
        print(f"{'='*60}")
        print(f"Reference String: {reference_string}")
        print(f"Frame Size: {frame_size}")
        print(f"{'='*60}")
        
        if algorithm_name.lower() == 'fifo':
            faults, steps = self.fifo_algorithm(reference_string, frame_size)
        elif algorithm_name.lower() == 'lru':
            faults, steps = self.lru_algorithm(reference_string, frame_size)
        elif algorithm_name.lower() == 'optimal':
            faults, steps = self.optimal_algorithm(reference_string, frame_size)
        else:
            faults, steps = self.custom_algorithm(reference_string, frame_size)
        
        print(f"\nStep-by-step execution:")
        print(f"{'Step':<4} {'Page':<4} {'Memory Frames':<20} {'Status':<10} {'Action'}")
        print("-" * 60)
        
        for i, step in enumerate(steps):
            frame_visual = "["
            for j in range(frame_size):
                if j < len(step['frames']):
                    frame_visual += f" {step['frames'][j]} "
                else:
                    frame_visual += " - "
                if j < frame_size - 1:
                    frame_visual += "|"
            frame_visual += "]"
            
            status = "PAGE FAULT" if step['fault'] else "PAGE HIT"
            action = "Load page" if step['fault'] and len(step['frames']) <= frame_size else "Replace page" if step['fault'] else "Page found"
            
            print(f"{i+1:<4} {step['page']:<4} {frame_visual:<20} {status:<10} {action}")
            
            time.sleep(0.5)
        
        print(f"\nSUMMARY:")
        print(f"Total Page Faults: {faults}")
        print(f"Total Page Hits: {len(steps) - faults}")
        print(f"Hit Ratio: {(len(steps) - faults)/len(steps)*100:.1f}%")
    
    def animated_demonstration(self, reference_string, frame_size):
        self.clear_screen()
        print(f"\n{'='*80}")
        print("ANIMATED COMPARISON: ALL ALGORITHMS")
        print(f"{'='*80}")
        print(f"Reference String: {reference_string}")
        print(f"Frame Size: {frame_size}")
        print(f"{'='*80}")
        
        results = self.simulate_all(reference_string, frame_size)
        
        print(f"\n{'Step':<4} {'Page':<4} {'FIFO':<15} {'LRU':<15} {'Optimal':<15} {'Custom':<15}")
        print("-" * 80)
        
        max_steps = len(reference_string)
        
        for i in range(max_steps):
            page = reference_string[i]
            
            representations = {}
            for alg_name, data in results.items():
                step = data['steps'][i]
                frame_visual = "["
                for j in range(frame_size):
                    if j < len(step['frames']):
                        frame_visual += f"{step['frames'][j]}"
                    else:
                        frame_visual += "-"
                    if j < frame_size - 1:
                        frame_visual += "|"
                frame_visual += "]"
                
                if step['fault']:
                    frame_visual += "*F"
                else:
                    frame_visual += " H"
                    
                representations[alg_name] = frame_visual
            
            print(f"{i+1:<4} {page:<4} {representations['FIFO']:<15} {representations['LRU']:<15} {representations['Optimal']:<15} {representations['Custom']:<15}")
            time.sleep(0.8)
        
        print(f"\nLegend: *F = Page Fault, H = Page Hit, - = Empty Slot")
        print(f"\nFINAL RESULTS:")
        for alg_name, data in results.items():
            print(f"{alg_name}: {data['faults']} page faults")
        
        return results
    
    def fifo_algorithm(self, reference_string, frame_size):
        frames = []
        page_faults = 0
        steps = []
        
        for page in reference_string:
            if page in frames:
                steps.append({'page': page, 'frames': frames.copy(), 'fault': False})
            else:
                page_faults += 1
                if len(frames) < frame_size:
                    frames.append(page)
                else:
                    frames.pop(0)
                    frames.append(page)
                steps.append({'page': page, 'frames': frames.copy(), 'fault': True})
        
        return page_faults, steps
    
    def lru_algorithm(self, reference_string, frame_size):
        frames = []
        page_faults = 0
        steps = []
        
        for page in reference_string:
            if page in frames:
                frames.remove(page)
                frames.append(page)
                steps.append({'page': page, 'frames': frames.copy(), 'fault': False})
            else:
                page_faults += 1
                if len(frames) < frame_size:
                    frames.append(page)
                else:
                    frames.pop(0)
                    frames.append(page)
                steps.append({'page': page, 'frames': frames.copy(), 'fault': True})
        
        return page_faults, steps
    
    def optimal_algorithm(self, reference_string, frame_size):
        frames = []
        page_faults = 0
        steps = []
        
        for i, page in enumerate(reference_string):
            if page in frames:
                steps.append({'page': page, 'frames': frames.copy(), 'fault': False})
            else:
                page_faults += 1
                if len(frames) < frame_size:
                    frames.append(page)
                else:
                    farthest = -1
                    page_to_remove = frames[0]
                    
                    for frame_page in frames:
                        try:
                            next_use = reference_string[i+1:].index(frame_page)
                        except ValueError:
                            next_use = float('inf')
                        
                        if next_use > farthest:
                            farthest = next_use
                            page_to_remove = frame_page
                    
                    frames.remove(page_to_remove)
                    frames.append(page)
                
                steps.append({'page': page, 'frames': frames.copy(), 'fault': True})
        
        return page_faults, steps
    
    def custom_algorithm(self, reference_string, frame_size):
        frames = []
        page_faults = 0
        steps = []
        frequency = defaultdict(int)
        access_time = {}
        
        for i, page in enumerate(reference_string):
            frequency[page] += 1
            
            if page in frames:
                access_time[page] = i
                steps.append({'page': page, 'frames': frames.copy(), 'fault': False})
            else:
                page_faults += 1
                if len(frames) < frame_size:
                    frames.append(page)
                    access_time[page] = i
                else:
                    highest_score = -float('inf')
                    page_to_remove = frames[0]
                    
                    for frame_page in frames:
                        last_access = access_time.get(frame_page, 0)
                        freq = frequency[frame_page]
                        
                        age = i - last_access
                        
                        score = age - (freq * 0.5)
                        
                        if score > highest_score:
                            highest_score = score
                            page_to_remove = frame_page
                    
                    frames.remove(page_to_remove)
                    frames.append(page)
                    access_time[page] = i
                
                steps.append({'page': page, 'frames': frames.copy(), 'fault': True})
    
        return page_faults, steps
    
    def simulate_all(self, reference_string, frame_size):
        results = {}
        
        fifo_faults, fifo_steps = self.fifo_algorithm(reference_string, frame_size)
        results['FIFO'] = {'faults': fifo_faults, 'steps': fifo_steps}
        
        lru_faults, lru_steps = self.lru_algorithm(reference_string, frame_size)
        results['LRU'] = {'faults': lru_faults, 'steps': lru_steps}
        
        optimal_faults, optimal_steps = self.optimal_algorithm(reference_string, frame_size)
        results['Optimal'] = {'faults': optimal_faults, 'steps': optimal_steps}
        
        custom_faults, custom_steps = self.custom_algorithm(reference_string, frame_size)
        results['Custom'] = {'faults': custom_faults, 'steps': custom_steps}
        
        return results
    
    def print_results(self, results, reference_string):
        self.clear_screen()
        print("\n" + "="*60)
        print("PAGE REPLACEMENT SIMULATION RESULTS")
        print("="*60)
        print(f"Reference String: {reference_string}")
        print("="*60)
        
        for alg_name, data in results.items():
            print(f"\n{alg_name} Algorithm:")
            print("-" * 30)
            print("Step | Page | Frames | Fault")
            print("-" * 30)
            
            for i, step in enumerate(data['steps']):
                fault_str = "YES" if step['fault'] else "NO"
                frames_str = str(step['frames']).replace('[', '').replace(']', '').replace(',', '')
                print(f"{i+1:4} | {step['page']:4} | {frames_str:10} | {fault_str}")
            
            print(f"\nTotal Page Faults: {data['faults']}")
    
    def plot_comparison(self, results, frame_size):
        algorithms = list(results.keys())
        page_faults = [results[alg]['faults'] for alg in algorithms]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        colors = ['blue', 'red', 'green', 'orange']
        bars = ax1.bar(algorithms, page_faults, color=colors)
        ax1.set_title('Page Faults Comparison')
        ax1.set_ylabel('Number of Page Faults')
        
        for bar, faults in zip(bars, page_faults):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{faults}', ha='center', va='bottom')
        
        for i, (alg_name, data) in enumerate(results.items()):
            cumulative = []
            count = 0
            for step in data['steps']:
                if step['fault']:
                    count += 1
                cumulative.append(count)
            
            ax2.plot(range(1, len(cumulative)+1), cumulative, 
                    label=alg_name, color=colors[i], marker='o')
        
        ax2.set_title('Cumulative Page Faults')
        ax2.set_xlabel('Reference Position')
        ax2.set_ylabel('Cumulative Faults')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle(f'Frame Size: {frame_size}')
        plt.tight_layout()
        
        print("Graph displayed. Press Enter in terminal to close...")
        plt.show(block=False)
        input()
        plt.close(fig)
        plt.close('all')
        plt.clf()
        plt.cla()
