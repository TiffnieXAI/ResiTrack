// -----------------------------
// Part 6: Household List Display
// -----------------------------

const fetchHouseholds = async () => {
    // 🔹 async: This function can pause while waiting for a response (from backend)
    
    try {
        const response = await axios.get(`${API}/households`);
        // 🔹 axios.get(): Makes an HTTP GET request to our API
        // 🔹 await: Waits for the server to respond before continuing
        // 🔹 ${API}/households: Full URL to the backend endpoint, e.g., "http://localhost:8000/households"

        setHouseholds(response.data);
        // 🔹 response.data: Array of household objects returned from backend
        // 🔹 setHouseholds(): Updates the React state variable to trigger UI re-render
        
    } catch (error) {
        console.error('Failed to fetch households:', error);
        // 🔹 catch: Runs if request fails (server down, network error)
        // 🔹 console.error(): Logs error to browser console
    }
};

// -----------------------------
// React State for Households
// -----------------------------
const [households, setHouseholds] = useState([]);
// 🔹 useState([]): Creates a state variable initialized to empty array
// 🔹 households: Current value of state (array of household objects)
// 🔹 setHouseholds: Function to update the state
// 🔹 When state updates, React re-renders the component automatically

// -----------------------------
// Part 7: Register Household Form
// -----------------------------
const handleCreateHousehold = async (e) => {
    e.preventDefault();
    // 🔹 e.preventDefault(): Stops the form from reloading the page (default behavior)
    
    try {
        const payload = {
            ...householdForm,
            // 🔹 ...householdForm: Copies all form input fields (name, address, latitude, longitude, contact, special_needs)
            
            latitude: parseFloat(householdForm.latitude),
            longitude: parseFloat(householdForm.longitude)
            // 🔹 parseFloat(): Converts string input to number
            // 🔹 Needed because backend expects numeric latitude and longitude
        };

        if (editingHousehold) {
            // 🔹 If editingHousehold exists, this is an update
            await axios.put(`${API}/households/${editingHousehold.id}`, payload);
            // 🔹 PUT request: Updates existing household by ID
            toast.success('Household updated successfully');
            // 🔹 Show success notification popup
        } else {
            // 🔹 Otherwise, this is a new household creation
            await axios.post(`${API}/households`, payload);
            // 🔹 POST request: Create new household
            toast.success('Household registered successfully');
        }

        setShowHouseholdDialog(false);
        // 🔹 Close the form dialog after success
        
        setEditingHousehold(null);
        // 🔹 Clear editing state

        setHouseholdForm({ 
            name: "", 
            address: "", 
            latitude: "", 
            longitude: "", 
            contact: "", 
            special_needs: "" 
        });
        // 🔹 Reset all form fields to empty strings

        fetchHouseholds();
        // 🔹 Refresh the household list to show new/updated entry

        fetchMetrics();
        // 🔹 Refresh dashboard metrics if any (optional)
        
    } catch (error) {
        toast.error('Failed to save household');
        console.error('Error saving household:', error);
        // 🔹 Shows error notification and logs detailed error
    }
};

// -----------------------------
// Part 8: Household Card Component
// -----------------------------
{households.map((household) => (
    // 🔹 .map(): Loop through each household in the array
    // 🔹 Returns JSX (HTML-like code) for each household card
    
    <Card key={household.id} className="household-card">
        {/* 🔹 key={household.id}: React needs a unique key for each element in a list */}
        <div className="household-header">
            <div className="household-title-section">
                <h3>{household.name}</h3>
                {/* 🔹 Display household name */}

                <span className={`status-badge status-${household.status}`}>
                    {/* 🔹 Dynamic class based on status: "safe", "not_safe", "unverified" */}
                    {household.status}
                    {/* 🔹 Display the safety status */}
                </span>
            </div>

            <div className="household-actions">
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => openEditHousehold(household)}
                    data-testid={`edit-household-${household.id}`}
                >
                    <Edit size={16} />
                    {/* 🔹 Edit button icon */}
                </Button>
                
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDeleteHousehold(household.id)}
                >
                    <Trash2 size={16} />
                    {/* 🔹 Delete button icon */}
                </Button>
            </div>
        </div>

        <div className="household-content">
            <p><strong>Address:</strong> {household.address}</p>
            <p><strong>Contact:</strong> {household.contact}</p>
            <p><strong>Coordinates:</strong> {household.latitude.toFixed(4)}, {household.longitude.toFixed(4)}</p>
            {/* 🔹 toFixed(4): Round coordinates to 4 decimal places */}

            {household.special_needs && (
                <p><strong>Special Needs:</strong> {household.special_needs}</p>
                // 🔹 Display only if special_needs exists
            )}
        </div>

        <div className="household-footer">
            <Button
                size="sm"
                variant={household.status === 'safe' ? 'outline' : 'default'}
                onClick={() => handleToggleStatus(household.id, 'safe')}
            >
                <Check size={16} /> Mark Safe
                {/* 🔹 Mark as safe button */}
            </Button>

            <Button
                size="sm"
                variant={household.status === 'not_safe' ? 'destructive' : 'outline'}
                onClick={() => handleToggleStatus(household.id, 'not_safe')}
            >
                <AlertCircle size={16} /> Mark Not Safe
                {/* 🔹 Mark as not safe button */}
            </Button>
        </div>
    </Card>
))}
