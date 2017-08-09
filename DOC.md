# Goals

## Distributions

 - [ ] Provide a consistent way to reference the current distribution's name.
 - [ ] Provide a consistent way to reference the current distribution's "base" (i.e. immediate parent) distribution.
 - [ ] Provide a consistent way to reference the current distribution's "root" (i.e. ultimate parent) distribution.

Use case:

```
# update the apt cache on ubuntu derivatives
- apt: update_cache=true cache_valid_time=3600
  when: naftulikay.base.distro.root.name == "ubuntu"
```

## Releases

 - [ ] Provide a consistent way to reference the current distribution's release name.
 - [ ] Provide a consistent way to reference the current distribution's "base" release name.
 - [ ] Provide a consistent way to reference the current distribution's "root" release name.

Use case:

```
# could be 'loki' or 'xenial'
- lineinfile: ... line="deb http://google.com {{ naftulikay.base.release.name }} stable"
# will always be 'xenial'
- lineinfile: ... line="deb http://google.com {{ naftulikay.base.release.root.name }} stable"
```
