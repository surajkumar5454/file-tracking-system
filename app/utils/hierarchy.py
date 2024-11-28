ROLE_HIERARCHY = {
    'BRANCH_DIARY': ['ESTATE_OFFICER'],
    'ESTATE_OFFICER': ['BUDGET_OFFICER'],
    'BUDGET_OFFICER': ['IFA'],
    'IFA': ['EE'],
    'EE': ['SE'],
    'SE': ['DIG'],
    'DIG': ['ADG'],
    'ADG': ['DG'],
    'DG': []  # Top of hierarchy
}

def get_subordinate_roles(role_name):
    """Get all roles that report to this role"""
    if not role_name:
        return []
        
    subordinates = []
    role_name = role_name.upper()
    
    def get_subordinates(current_role):
        for role, superiors in ROLE_HIERARCHY.items():
            if current_role in superiors:
                subordinates.append(role)
                get_subordinates(role)
    
    get_subordinates(role_name)
    return subordinates

def get_superior_roles(role_name):
    """Get all roles above this role in hierarchy"""
    if not role_name:
        return []
        
    role_name = role_name.upper()
    superiors = []
    current_role = role_name
    
    while current_role in ROLE_HIERARCHY:
        superior = ROLE_HIERARCHY[current_role]
        if not superior:  # Reached top
            break
        superiors.extend(superior)
        current_role = superior[0]
    
    return superiors

def can_access_proposal(user, proposal):
    # DG and ADG can access all proposals
    if user.role.name in ['DG', 'ADG']:
        return True
    
    # Users can access proposals from their department
    if proposal.department == user.department:
        return True
    
    # Users can access proposals if they're in the movement chain
    movements = proposal.movements
    departments = [m.to_department for m in movements] + [m.from_department for m in movements]
    if user.department in departments:
        return True
    
    return False