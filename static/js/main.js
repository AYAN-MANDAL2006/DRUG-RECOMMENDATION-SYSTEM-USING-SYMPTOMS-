/*
  static/js/main.js
  Client-side interaction script for Drug Recommendation System.
  Handles live symptom search, multi-selection chip management,
  and dynamic synchronization with the natural language analysis form.
*/

document.addEventListener('DOMContentLoaded', function() {
    const symptomInput = document.getElementById('symptoms-input');
    const clearBtn = document.getElementById('clear-btn');
    const searchInput = document.getElementById('symptom-search-input');
    const searchClearBtn = document.getElementById('search-clear-btn');
    const searchResultsContainer = document.getElementById('symptom-search-results');
    const searchStatusBar = document.getElementById('search-status-bar');
    const searchResultsCount = document.getElementById('search-results-count');
    const selectedTray = document.getElementById('selected-symptoms-tray');
    const selectedCountBadge = document.getElementById('selected-count-badge');
    const clearSelectedBtn = document.getElementById('clear-selected-btn');
    const noSymptomsHint = document.getElementById('no-symptoms-hint');
    const quickSymptomTags = document.querySelectorAll('.symptom-tag');

    // Multi-selected symptoms set
    const selectedSymptoms = new Set();

    // Debounce timer reference
    let debounceTimer = null;

    /**
     * Updates the Selected Symptoms Tray UI and synchronizes with textarea
     */
    function updateSelectedUI() {
        if (!selectedTray) return;

        // Clear existing chips
        selectedTray.innerHTML = '';

        if (selectedSymptoms.size === 0) {
            if (noSymptomsHint) {
                selectedTray.appendChild(noSymptomsHint);
                noSymptomsHint.style.display = 'inline';
            }
            if (selectedCountBadge) selectedCountBadge.style.display = 'none';
            if (clearSelectedBtn) clearSelectedBtn.style.display = 'none';
        } else {
            if (selectedCountBadge) {
                selectedCountBadge.textContent = selectedSymptoms.size;
                selectedCountBadge.style.display = 'inline-block';
            }
            if (clearSelectedBtn) clearSelectedBtn.style.display = 'inline-block';

            selectedSymptoms.forEach(symptom => {
                const chip = document.createElement('span');
                chip.className = 'selected-chip';
                chip.innerHTML = `
                    <span>${escapeHtml(symptom)}</span>
                    <button type="button" class="chip-remove-btn" data-symptom="${escapeHtml(symptom)}" title="Remove symptom">×</button>
                `;

                chip.querySelector('.chip-remove-btn').addEventListener('click', function(e) {
                    e.stopPropagation();
                    removeSymptom(symptom);
                });

                selectedTray.appendChild(chip);
            });
        }

        // Sync to form input
        if (symptomInput) {
            const currentList = Array.from(selectedSymptoms);
            symptomInput.value = currentList.join(', ');
        }

        // Update active class on search results and quick tags
        updateChipActiveStates();
    }

    /**
     * Updates visual active/selected state across search chips and quick tags
     */
    function updateChipActiveStates() {
        // Search chips
        document.querySelectorAll('.search-match-chip').forEach(chip => {
            const sym = chip.getAttribute('data-symptom');
            if (selectedSymptoms.has(sym)) {
                chip.classList.add('selected');
            } else {
                chip.classList.remove('selected');
            }
        });

        // Quick tags
        document.querySelectorAll('.symptom-tag').forEach(tag => {
            const sym = tag.getAttribute('data-symptom');
            if (selectedSymptoms.has(sym)) {
                tag.style.backgroundColor = '#0f766e';
                tag.style.color = '#ffffff';
            } else {
                tag.style.backgroundColor = '';
                tag.style.color = '';
            }
        });
    }

    /**
     * Adds a symptom to the selected set
     */
    function addSymptom(symptom) {
        if (!symptom || !symptom.trim()) return;
        selectedSymptoms.add(symptom.trim());
        updateSelectedUI();
    }

    /**
     * Removes a symptom from the selected set
     */
    function removeSymptom(symptom) {
        if (!symptom) return;
        selectedSymptoms.delete(symptom);
        updateSelectedUI();
    }

    /**
     * Toggles a symptom in the selected set
     */
    function toggleSymptom(symptom) {
        if (!symptom) return;
        if (selectedSymptoms.has(symptom)) {
            removeSymptom(symptom);
        } else {
            addSymptom(symptom);
        }
    }

    /**
     * Performs live AJAX search against /api/symptoms/search
     */
    function performLiveSearch(query) {
        if (!query || !query.trim()) {
            if (searchResultsContainer) searchResultsContainer.innerHTML = '';
            if (searchStatusBar) searchStatusBar.style.display = 'none';
            if (searchClearBtn) searchClearBtn.style.display = 'none';
            return;
        }

        if (searchClearBtn) searchClearBtn.style.display = 'inline-block';

        fetch(`/api/symptoms/search?q=${encodeURIComponent(query.trim())}`)
            .then(res => res.json())
            .then(data => {
                if (!searchResultsContainer) return;
                searchResultsContainer.innerHTML = '';

                const results = data.results || [];
                const count = results.length;

                if (searchStatusBar && searchResultsCount) {
                    searchStatusBar.style.display = 'flex';
                    searchResultsCount.textContent = `${count} matching symptom${count === 1 ? '' : 's'} found`;
                }

                if (count === 0) {
                    searchResultsContainer.innerHTML = `
                        <div style="font-size: 0.85rem; color: var(--text-muted); padding: 0.5rem 0;">
                            No matching symptoms found for "${escapeHtml(query)}". You can still enter custom symptoms in the box below.
                        </div>
                    `;
                    return;
                }

                // Render all matching symptoms without unnecessary limits
                results.forEach(item => {
                    const isSelected = selectedSymptoms.has(item.symptom_name);
                    const chip = document.createElement('div');
                    chip.className = `search-match-chip ${isSelected ? 'selected' : ''}`;
                    chip.setAttribute('data-symptom', item.symptom_name);
                    chip.setAttribute('data-id', item.symptom_id);

                    let hintHtml = '';
                    if (item.matched_by && item.matched_by.includes('search_terms') && !item.matched_by.includes('name')) {
                        hintHtml = `<span class="matched-hint">via synonyms</span>`;
                    }

                    chip.innerHTML = `
                        <span class="match-name">${isSelected ? '✓' : '+'} ${escapeHtml(item.symptom_name)}</span>
                        <span class="category-badge">${escapeHtml(item.category || 'General')}</span>
                        ${hintHtml}
                    `;

                    chip.addEventListener('click', function() {
                        toggleSymptom(item.symptom_name);
                    });

                    searchResultsContainer.appendChild(chip);
                });
            })
            .catch(err => {
                console.error("Symptom search failed:", err);
            });
    }

    // Input event for live symptom search with 200ms debounce
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            const q = this.value;
            debounceTimer = setTimeout(() => {
                performLiveSearch(q);
            }, 200);
        });

        // Trigger on load if searchInput already has value (e.g. from server redirect)
        if (searchInput.value.trim()) {
            performLiveSearch(searchInput.value.trim());
        }
    }

    // Clear search input button
    if (searchClearBtn && searchInput) {
        searchClearBtn.addEventListener('click', function() {
            searchInput.value = '';
            performLiveSearch('');
            searchInput.focus();
        });
    }

    // Quick popular symptom tags click handler
    quickSymptomTags.forEach(tag => {
        tag.addEventListener('click', function() {
            const symptomText = this.getAttribute('data-symptom') || this.textContent.replace('+', '').trim();
            toggleSymptom(symptomText);
        });
    });

    // Clear Selected button
    if (clearSelectedBtn) {
        clearSelectedBtn.addEventListener('click', function() {
            selectedSymptoms.clear();
            updateSelectedUI();
        });
    }

    // Main Reset All button handler
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            selectedSymptoms.clear();
            updateSelectedUI();
            if (symptomInput) symptomInput.value = '';
            if (searchInput) {
                searchInput.value = '';
                performLiveSearch('');
            }
        });
    }

    // Helper: HTML sanitization for rendering text safely
    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }
});
