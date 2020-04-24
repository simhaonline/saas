package com.tomale.saas.modules.admin.security.controllers;

import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.security.access.prepost.PreAuthorize;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.tomale.saas.base.models.ApiResult;
import com.tomale.saas.modules.admin.security.Role;
import com.tomale.saas.modules.admin.security.store.AdminRoleStore;


@RestController
@RequestMapping("/api/admin/security/roles")
public class RestRoleController {

    private static final Logger log = LogManager.getLogger(RestRoleController.class);

    @Autowired
    private AdminRoleStore adminRoleStore;

    @PostMapping("/all")
    @PreAuthorize("hasPermission(#user, 'admin.security.roles')")
    public ApiResult getAllRoles(Map<String, Object> data) {
        try {
            String clientId = data.get("clientId").toString();
            List<Role> roles = adminRoleStore.getRoles(UUID.fromString(clientId));

            Gson gson = new Gson();

            return new ApiResult(
                "success",
                String.format("%d roles retrieved", roles.size()),
                gson.toJson(roles)
            );
        } catch(Exception e) {
            log.error(e);

            return new ApiResult(
                "error",
                "An error occured while trying to retrieve roles",
                null
            );
        }
    }
}