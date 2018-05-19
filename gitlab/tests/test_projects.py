def test_projects(gitlab):
    projects = gitlab.get('/projects')

    anyproj = projects[0]
    assert anyproj['ssh_url_to_repo'].startswith('git@')
    assert anyproj['http_url_to_repo'].startswith('https://')