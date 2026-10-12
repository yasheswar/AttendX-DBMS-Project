import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_er_diagram():
    fig, ax = plt.subplots(figsize=(19, 11), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")
    
    # Title Header Banner
    fig.text(0.5, 0.96, "AttendX: Entity-Relationship Diagram (3NF Relational Architecture)", 
             fontsize=20, weight="bold", color="#1E293B", ha="center")
    fig.text(0.5, 0.935, "School of Technology, Woxsen University | B.Tech CSE (Academic Year 2026-27)", 
             fontsize=11, color="#64748B", ha="center")

    # Entity definition structure:
    # name: (x, y, width, height, header_bg, [attributes])
    entities = {
        "USERS": (1.0, 7.2, 2.6, 1.8, "#3B82F6", [
            ("user_id", "INT", "PK"),
            ("username", "VARCHAR(50)", "U"),
            ("password_hash", "VARCHAR(255)", ""),
            ("role", "ENUM('ADM','FAC','STU')", "")
        ]),
        "STUDENTS": (4.6, 7.0, 3.0, 2.2, "#2563EB", [
            ("student_id", "INT", "PK"),
            ("user_id", "INT", "FK"),
            ("registration_number", "VARCHAR(20)", "U"),
            ("first_name", "VARCHAR(50)", ""),
            ("email", "VARCHAR(100)", "U"),
            ("department", "VARCHAR(50)", ""),
            ("semester", "INT", "")
        ]),
        "FACULTY": (1.0, 3.8, 2.8, 2.2, "#2563EB", [
            ("faculty_id", "INT", "PK"),
            ("user_id", "INT", "FK"),
            ("faculty_code", "VARCHAR(20)", "U"),
            ("first_name", "VARCHAR(50)", ""),
            ("email", "VARCHAR(100)", "U"),
            ("department", "VARCHAR(50)", ""),
            ("designation", "VARCHAR(50)", "")
        ]),
        "COURSES": (4.8, 3.8, 2.7, 1.8, "#6366F1", [
            ("course_id", "INT", "PK"),
            ("course_code", "VARCHAR(20)", "U"),
            ("course_name", "VARCHAR(100)", ""),
            ("credits", "INT", "")
        ]),
        "SECTIONS": (4.8, 0.8, 2.7, 1.8, "#6366F1", [
            ("section_id", "INT", "PK"),
            ("section_name", "VARCHAR(20)", ""),
            ("semester", "INT", ""),
            ("academic_year", "VARCHAR(9)", "")
        ]),
        "STUDENT_SECTION": (1.0, 0.8, 2.8, 1.8, "#0D9488", [
            ("student_section_id", "INT", "PK"),
            ("student_id", "INT", "FK"),
            ("section_id", "INT", "FK"),
            ("academic_year", "VARCHAR(9)", "")
        ]),
        "COURSE_OFFERINGS": (8.6, 3.5, 3.1, 2.5, "#0D9488", [
            ("offering_id", "INT", "PK"),
            ("course_id", "INT", "FK"),
            ("section_id", "INT", "FK"),
            ("faculty_id", "INT", "FK"),
            ("academic_year", "VARCHAR(9)", ""),
            ("semester", "INT", "")
        ]),
        "CLASS_SESSIONS": (12.8, 3.5, 2.9, 2.5, "#D97706", [
            ("session_id", "INT", "PK"),
            ("offering_id", "INT", "FK"),
            ("session_date", "DATE", ""),
            ("start_time", "TIME", ""),
            ("end_time", "TIME", ""),
            ("session_status", "ENUM", "")
        ]),
        "ATTENDANCE": (12.8, 7.0, 3.0, 2.3, "#DC2626", [
            ("attendance_id", "INT", "PK"),
            ("session_id", "INT", "FK, U1"),
            ("student_id", "INT", "FK, U1"),
            ("attendance_status", "ENUM", ""),
            ("marked_at", "TIMESTAMP", ""),
            ("remarks", "VARCHAR(255)", "")
        ]),
        "MAKEUP_SESSIONS": (16.7, 3.5, 2.8, 2.2, "#D97706", [
            ("makeup_id", "INT", "PK"),
            ("original_session_id", "INT", "FK"),
            ("makeup_session_id", "INT", "FK"),
            ("created_by", "INT", "FK"),
            ("reason", "VARCHAR(255)", "")
        ]),
        "LEAVE_TYPES": (8.8, 8.4, 2.6, 1.5, "#9333EA", [
            ("leave_type_id", "INT", "PK"),
            ("leave_type_name", "VARCHAR(50)", "U"),
            ("max_days", "INT", "")
        ]),
        "LEAVE_APPLICATIONS": (8.6, 6.0, 3.2, 2.1, "#9333EA", [
            ("application_id", "INT", "PK"),
            ("student_id", "INT", "FK"),
            ("leave_type_id", "INT", "FK"),
            ("from_date", "DATE", ""),
            ("to_date", "DATE", ""),
            ("application_status", "ENUM", "")
        ]),
        "LEAVE_APPROVALS": (8.6, 0.8, 3.1, 2.1, "#9333EA", [
            ("approval_id", "INT", "PK"),
            ("application_id", "INT", "FK"),
            ("faculty_id", "INT", "FK"),
            ("approval_status", "ENUM", ""),
            ("approved_at", "TIMESTAMP", "")
        ]),
        "ALERTS": (16.7, 7.0, 2.8, 2.2, "#DC2626", [
            ("alert_id", "INT", "PK"),
            ("student_id", "INT", "FK"),
            ("offering_id", "INT", "FK"),
            ("alert_type", "ENUM", ""),
            ("attendance_percentage", "DECIMAL", "")
        ])
    }

    # Render Entities
    for name, (x, y, w, h, bg_color, attrs) in entities.items():
        # Outer Card
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.1",
                                      facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.5, zorder=2)
        ax.add_patch(card)
        
        # Header Box
        hdr_h = 0.42
        hdr = patches.FancyBboxPatch((x, y + h - hdr_h), w, hdr_h, 
                                     boxstyle="round,pad=0.04,rounding_size=0.1",
                                     facecolor=bg_color, edgecolor=bg_color, linewidth=1, zorder=3)
        ax.add_patch(hdr)
        
        # Header Text
        ax.text(x + w/2, y + h - hdr_h/2, name, color="#FFFFFF", fontsize=10, 
                weight="bold", ha="center", va="center", zorder=4)

        # Attribute text inside card
        line_y = y + h - hdr_h - 0.22
        for col, dtype, key in attrs:
            # Key badge
            if "PK" in key:
                ax.text(x + 0.15, line_y, "PK", color="#D97706", fontsize=7.5, weight="bold", zorder=4)
            elif "FK" in key:
                ax.text(x + 0.15, line_y, "FK", color="#2563EB", fontsize=7.5, weight="bold", zorder=4)
            elif "U" in key:
                ax.text(x + 0.15, line_y, "U", color="#059669", fontsize=7.5, weight="bold", zorder=4)
            else:
                ax.text(x + 0.15, line_y, "•", color="#94A3B8", fontsize=8, weight="bold", zorder=4)

            # Column Name
            ax.text(x + 0.48, line_y, col, color="#1E293B", fontsize=8, weight="bold" if key else "normal", zorder=4)
            # Data Type
            ax.text(x + w - 0.15, line_y, dtype, color="#64748B", fontsize=7.5, ha="right", zorder=4)
            
            line_y -= 0.25

    # Relationship connector lines & cardinalities (Crow's foot style)
    def draw_rel(ptA, ptB, cardA="1", cardB="*", label="", color="#475569", style="-"):
        ax.plot([ptA[0], ptB[0]], [ptA[1], ptB[1]], color=color, linestyle=style, linewidth=1.6, zorder=1)
        # Cardinality text tags
        mid_x = (ptA[0] + ptB[0]) / 2
        mid_y = (ptA[1] + ptB[1]) / 2
        
        # Text at ends
        ax.text(ptA[0] + (mid_x - ptA[0])*0.25, ptA[1] + (mid_y - ptA[1])*0.25, cardA, 
                fontsize=8, weight="bold", color="#1E293B", bbox=dict(boxstyle="round,pad=0.15", facecolor="#F1F5F9", edgecolor="none"))
        ax.text(ptB[0] + (mid_x - ptB[0])*0.25, ptB[1] + (mid_y - ptB[1])*0.25, cardB, 
                fontsize=8, weight="bold", color="#1E293B", bbox=dict(boxstyle="round,pad=0.15", facecolor="#F1F5F9", edgecolor="none"))
        if label:
            ax.text(mid_x, mid_y, label, fontsize=7.5, color="#0F172A", weight="bold", 
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="#FEF08A", edgecolor="#E2E8F0", alpha=0.9), ha="center", va="center", zorder=5)

    # 1. USERS -> STUDENTS & FACULTY
    draw_rel((2.3, 7.2), (4.6, 8.1), "1", "0..1", "specializes", color="#3B82F6")
    draw_rel((2.3, 7.2), (2.3, 6.0), "1", "0..1", "specializes", color="#3B82F6")

    # 2. STUDENTS <-> SECTIONS via STUDENT_SECTION (M:N)
    draw_rel((4.6, 7.2), (2.8, 2.6), "1", "1..*", "enrolls", color="#0D9488")
    draw_rel((4.8, 1.7), (3.8, 1.7), "1", "1..*", "contains", color="#0D9488")

    # 3. COURSES, SECTIONS, FACULTY -> COURSE_OFFERINGS (Ternary M:N)
    draw_rel((7.5, 4.7), (8.6, 4.7), "1", "1..*", "offered as", color="#6366F1")
    draw_rel((7.5, 1.7), (8.6, 3.8), "1", "1..*", "scheduled for", color="#6366F1")
    draw_rel((3.8, 4.9), (8.6, 5.2), "1", "1..*", "teaches", color="#2563EB")

    # 4. COURSE_OFFERINGS -> CLASS_SESSIONS
    draw_rel((11.7, 4.7), (12.8, 4.7), "1", "1..*", "conducts", color="#D97706")

    # 5. CLASS_SESSIONS & STUDENTS -> ATTENDANCE (M:N Bridge)
    draw_rel((14.2, 6.0), (14.2, 7.0), "1", "1..*", "records", color="#DC2626")
    draw_rel((7.6, 8.1), (12.8, 8.1), "1", "1..*", "marked for (M:N)", color="#DC2626")

    # 6. CLASS_SESSIONS -> MAKEUP_SESSIONS
    draw_rel((15.7, 4.7), (16.7, 4.7), "1", "0..1", "compensated by", color="#D97706")

    # 7. LEAVE WORKFLOW: STUDENTS -> LEAVE_APPLICATIONS -> LEAVE_APPROVALS
    draw_rel((7.6, 7.6), (8.6, 7.6), "1", "1..*", "submits", color="#9333EA")
    draw_rel((10.1, 8.4), (10.1, 8.1), "1", "1..*", "classified by", color="#9333EA")
    draw_rel((10.1, 6.0), (10.1, 2.9), "1", "0..1", "reviewed via (1:1)", color="#9333EA")
    draw_rel((3.8, 4.2), (8.6, 1.8), "1", "1..*", "approves", color="#9333EA")

    # 8. ALERTS
    draw_rel((7.6, 8.7), (16.7, 8.7), "1", "1..*", "triggers alert", color="#EF4444", style="--")

    # Legend & Key Box
    leg_patch = patches.FancyBboxPatch((13.5, 0.6), 5.8, 1.7, boxstyle="round,pad=0.05",
                                      facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2, zorder=2)
    ax.add_patch(leg_patch)
    ax.text(13.7, 2.05, "ACADEMIC ARCHITECTURAL HIGHLIGHTS:", fontsize=8.5, weight="bold", color="#1E293B", zorder=3)
    ax.text(13.7, 1.75, "• 15 Tables Normalized up to 3NF & BCNF", fontsize=8, color="#475569", zorder=3)
    ax.text(13.7, 1.50, "• M:N Student <-> Session resolved via ATTENDANCE", fontsize=8, color="#0284C7", weight="bold", zorder=3)
    ax.text(13.7, 1.25, "• Ternary Association: COURSE_OFFERINGS (Course+Sec+Fac)", fontsize=8, color="#0D9488", weight="bold", zorder=3)
    ax.text(13.7, 1.00, "• Composite Unique Constraint: UNIQUE(session_id, student_id)", fontsize=8, color="#DC2626", weight="bold", zorder=3)
    ax.text(13.7, 0.75, "• Automated Triggers: Shortage Alerts & Absence Reconciliation", fontsize=8, color="#9333EA", weight="bold", zorder=3)

    ax.set_xlim(0.2, 20.0)
    ax.set_ylim(0.2, 10.0)
    ax.axis("off")
    
    out_path = "docs/AttendX_ER_Diagram_Slide8.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"High-resolution ER diagram generated at: {out_path}")

if __name__ == "__main__":
    draw_er_diagram()
