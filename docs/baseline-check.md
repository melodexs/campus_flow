# CampusFlow Next — Baseline Check

## Environment

- Repository: https://github.com/melodexs/campus_flow
- Baseline branch: `main`
- Working tree at baseline: clean
- Baseline commit: Record the output of `git rev-parse HEAD`
- Test command: `python3 -m unittest discover -s tests -v`

## Baseline Test Results

- Tests run: 52
- Passed: 52
- Failed: 0
- Result: OK

## Existing Features Verified by Tests

1. Ticket creation and priority calculation.
2. Ticket assignment and status transitions.
3. Work queue sorting and filtering.
4. Ticket reports.
5. JSON ticket storage and loading.
6. CLI ticket viewing and clean EOF handling.

## Initial Observations

1. Existing tests cover ticket creation, priority calculations,
   workflow, reports, storage and CLI behaviour.
2. Existing work queue tests expect open and in-progress tickets
   to be included. CampusFlow Next requires only open tickets,
   so this behaviour needs a targeted regression test and correction.
3. Additional requirements include structured notes, combined
   search filters, comprehensive JSON validation and ticket/note
   ID continuity.

## Manual Checks

Three manual application input/output checks still need to be
identified or completed. Record each action, its expected result
and its actual result here.

## Limitations

The recorded results describe the original baseline test suite.
The original audited commit and three manual CLI checks still
need to be identified or completed.

## Improvements Required by CampusFlow Next

1. Centralize and strengthen ticket validation.
2. Prevent invalid operations from modifying ticket data.
3. Add ticket follow-up notes with persistent note IDs.
4. Strengthen JSON validation and preserve existing in-memory
   data if loading invalid data fails.
5. Ensure ticket and note IDs remain unique after reloading.
6. Implement the agreed search filters and verify their behaviour.

## Next Action

Identify the audited baseline commit, verify the original baseline
where available, and complete the agreed feature issues on
separate branches.