// -----------------------------
// Part 4: Frontend - Incident Form
// /app/frontend/src/App.js (lines 138-172)
// -----------------------------

const handleCreateIncident = async (e) => {
    e.preventDefault();
    // 🔹 Prevent default form submission behavior
    // 🔹 Normally, submitting a form reloads the page
    // 🔹 We don’t want that in a SPA (Single Page App)

    try {
        const payload = {
            ...incidentForm,
            // 🔹 Spread operator "..." copies all fields from incidentForm
            // 🔹 Example: type, phase, severity, description, affected_area, etc.

            affected_families: parseInt(incidentForm.affected_families),
            relief_distributed: parseInt(incidentForm.relief_distributed)
            // 🔹 HTML input values are always strings
            // 🔹 parseInt converts them to integers
            // 🔹 API expects numbers, otherwise backend might error
        };

        if (editingIncident) {
            // 🔹 If editingIncident exists, user is updating an existing incident
            await axios.put(`${API}/incidents/${editingIncident.id}`, payload);
            // 🔹 axios.put(): HTTP PUT request to update the incident
            toast.success('Incident updated successfully');
            // 🔹 Show success popup using "toast"
        } else {
            // 🔹 Otherwise, user is creating a NEW incident
            await axios.post(`${API}/incidents`, payload);
            // 🔹 axios.post(): HTTP POST request to create a new incident
            toast.success('Incident created successfully');
        }

        setShowIncidentDialog(false);
        // 🔹 Close the create/edit form dialog

        setEditingIncident(null);
        // 🔹 Clear editing state, so next time it defaults to creation

        setIncidentForm({
            type: "flood",
            phase: "incoming",
            severity: "medium",
            description: "",
            affected_area: "",
            affected_families: 0,
            relief_distributed: 0
        });
        // 🔹 Reset form fields to default values for next entry

        fetchIncidents();
        fetchMetrics();
        // 🔹 Refresh the incident list to show new/updated incidents
        // 🔹 Refresh dashboard metrics like total affected families
    } catch (error) {
        toast.error('Failed to save incident');
        console.error('Error saving incident:', error);
        // 🔹 Log any errors for debugging
    }
};

// -----------------------------
// Part 5: Frontend - Incident Card Display
// /app/frontend/src/App.js (lines 776-819)
// -----------------------------

{incidents.map((incident) => (
    // 🔹 Loop through all incidents and create a card for each
    // 🔹 .map() returns an array of JSX elements

    <Card key={incident.id} className="incident-card">
        {/* 🔹 key={incident.id}: React requires unique keys for list elements */}
        {/* 🔹 Helps React efficiently update/re-render only changed items */}

        <div className="incident-header">
            <div className="incident-title-section">
                <h3>{incident.type.toUpperCase()}</h3>
                {/* 🔹 Convert disaster type to uppercase for emphasis */}

                <div className="incident-badges">
                    <span className={`phase-badge ${getPhaseColor(incident.phase)}`}>
                        {/* 🔹 Badge color based on phase */}
                        {incident.phase}
                        {/* 🔹 Display current phase: incoming, occurring, past */}
                    </span>

                    <span className={`severity-badge ${getSeverityColor(incident.severity)}`}>
                        {/* 🔹 Badge color based on severity */}
                        {incident.severity}
                        {/* 🔹 Display severity level: low, medium, high, critical */}
                    </span>
                </div>
            </div>

            <div className="incident-actions">
                <Button onClick={() => openEditIncident(incident)}>
                    {/* 🔹 Opens form pre-filled with incident data for editing */}
                    <Edit size={16} />
                    {/* 🔹 Pencil icon */}
                </Button>
                <Button onClick={() => handleDeleteIncident(incident.id)}>
                    {/* 🔹 Delete incident */}
                    <Trash2 size={16} />
                </Button>
            </div>
        </div>

        <div className="incident-content">
            <p><strong>Area:</strong> {incident.affected_area}</p>
            {/* 🔹 Shows affected geographic area */}
            
            <p><strong>Description:</strong> {incident.description}</p>
            {/* 🔹 Shows full disaster details */}

            <div className="incident-stats">
                {/* 🔹 Stats section */}
                <div className="stat">
                    <span className="stat-label">Affected Families</span>
                    <span className="stat-value">{incident.affected_families}</span>
                    {/* 🔹 Number of families impacted */}
                </div>

                <div className="stat">
                    <span className="stat-label">Relief Distributed</span>
                    <span className="stat-value">{incident.relief_distributed}</span>
                    {/* 🔹 Number of families who received aid */}
                </div>
            </div>
        </div>
    </Card>
))}

// -----------------------------
// Part 6: Frontend - Color Coding Functions
// /app/frontend/src/App.js (lines 251-273)
// -----------------------------

const getSeverityColor = (severity) => {
    // 🔹 Converts severity text to CSS class for color coding
    switch (severity) {
        case 'critical':
            return 'bg-red-600'; // 🔹 Immediate danger, red
        case 'high':
            return 'bg-orange-600'; // 🔹 High risk, orange
        case 'medium':
            return 'bg-yellow-600'; // 🔹 Medium risk, yellow
        default:
            return 'bg-blue-600'; // 🔹 Low risk or informational, blue
    }
};

const getPhaseColor = (phase) => {
    // 🔹 Converts phase text to CSS class for color coding
    switch (phase) {
        case 'occurring':
            return 'bg-red-600'; // 🔹 Disaster happening now
        case 'incoming':
            return 'bg-orange-600'; // 🔹 Disaster approaching
        default:
            return 'bg-gray-600'; // 🔹 Past incident
    }
};
