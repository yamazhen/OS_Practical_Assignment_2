from simulator import Simulator


def main():
    simulator = Simulator()
    simulator.clear_screen()
    
    print("PAGE FAULT SIMULATION SYSTEM")
    print("Operating Systems Assignment")
    print("="*40)
    
    while True:
        print("\nOptions:")
        print("1. Custom input")
        print("2. Test cases")
        print("3. Visual demonstration (single algorithm)")
        print("4. Animated comparison (all algorithms)")
        print("5. Exit")
        
        choice = input("Choose option (1-5): ")
        
        if choice == '1':
            try:
                simulator.clear_screen()
                ref_input = input("Enter reference string (space-separated): ")
                reference_string = list(map(int, ref_input.split()))
                frame_size = int(input("Enter frame size: "))
                
                results = simulator.simulate_all(reference_string, frame_size)
                simulator.print_results(results, reference_string)
                
                show_graph = input("\nShow graphs? (y/n): ")
                if show_graph.lower() == 'y':
                    simulator.plot_comparison(results, frame_size)
                
                input("\nPress Enter to continue...")
                simulator.clear_screen()
                
            except ValueError:
                print("Invalid input! Please enter numbers only.")
                input("Press Enter to continue...")
                simulator.clear_screen()
        
        elif choice == '2':
            simulator.clear_screen()
            test_cases = [
                ([7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2], 3),
                ([1, 3, 0, 3, 5, 6, 3], 3),
                ([2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2], 4)
            ]
            
            print("Test Cases:")
            for i, (ref_str, frames) in enumerate(test_cases, 1):
                print(f"{i}. {ref_str}, frames={frames}")
            
            try:
                test_num = int(input("Select test case (1-3): ")) - 1
                if 0 <= test_num < len(test_cases):
                    reference_string, frame_size = test_cases[test_num]
                    
                    results = simulator.animated_demonstration(reference_string, frame_size)
                    
                    input("\nPress Enter to show graphs...")
                    simulator.clear_screen()
                    
                    simulator.plot_comparison(results, frame_size)
                else:
                    print("Invalid test case!")
                
                input("\nPress Enter to continue...")
                simulator.clear_screen()
                
            except ValueError:
                print("Invalid input!")
                input("Press Enter to continue...")
                simulator.clear_screen()
        
        elif choice == '3':
            try:
                simulator.clear_screen()
                ref_input = input("Enter reference string (space-separated): ")
                reference_string = list(map(int, ref_input.split()))
                frame_size = int(input("Enter frame size: "))
                
                print("\nSelect algorithm:")
                print("1. FIFO")
                print("2. LRU") 
                print("3. Optimal")
                print("4. Custom")
                
                alg_choice = input("Choose algorithm (1-4): ")
                algorithms = {'1': 'fifo', '2': 'lru', '3': 'optimal', '4': 'custom'}
                
                if alg_choice in algorithms:
                    simulator.clear_screen()
                    simulator.visual_demonstration(reference_string, frame_size, algorithms[alg_choice])
                else:
                    print("Invalid choice!")
                
                input("\nPress Enter to continue...")
                simulator.clear_screen()
                
            except ValueError:
                print("Invalid input!")
                input("Press Enter to continue...")
                simulator.clear_screen()
        
        elif choice == '4':
            try:
                simulator.clear_screen()
                ref_input = input("Enter reference string (space-separated): ")
                reference_string = list(map(int, ref_input.split()))
                frame_size = int(input("Enter frame size: "))
                
                simulator.animated_demonstration(reference_string, frame_size)
                
                input("\nPress Enter to continue...")
                simulator.clear_screen()
                
            except ValueError:
                print("Invalid input!")
                input("Press Enter to continue...")
                simulator.clear_screen()
        
        elif choice == '5':
            simulator.clear_screen()
            print("Thank you!")
            break
        
        else:
            print("Invalid choice!")
            input("Press Enter to continue...")
            simulator.clear_screen()

if __name__ == "__main__":
    main()
